def get_destinations(query):
    destinations_params = {}
    destinations_sql = ""

    roomNumber = query.room_number
    buildingName = query.building_name
    address = query.address
    floorNumber = query.floor_number
    accessibility = query.accessibility
    featureType = query.feature_type
    roomDescription = query.room_description

    # Building and adress related things might be there but not relevant rn
    if buildingName is not None:
        pass

    if address is not None:
        pass

    # This function needs to filter destinations based on all the query params (structured output)
    if roomNumber is not None:
        room_number = {"room_number": roomNumber}
        destinations_params.update(room_number)
        destinations_sql = """ 
        specific_room AS (
            SELECT indoor_space_id AS id,
            geom, floor_id FROM indoor_space 
                WHERE room_number=%(room_number)s),
        """
        return destinations_sql,destinations_params

    raise HTTPException(
        status_code=400,
        detail="Could not determine a destination"
    )


def accessibility_sql(accessibility_bool):
    accessibility_params = {}
    accessibility_bool = {"accessibility_bool": accessibility_bool}
    accessibility_params.update(accessibility_bool)
    
    accessibility_sql = """ 
    specific_room AS (
        SELECT indoor_space_id AS id,
        geom, floor_id FROM indoor_space 
            WHERE room_number=%(room_number)s),
    """
    return accessibility_sql,accessibility_params

def get_start_location(startLocation):
    point = startLocation.point
    floor = startLocation.floor
    return """
    start_location AS (
            SELECT 0 AS id,
            ST_SetSRID(ST_MakePoint(%(start_x)s, %(start_y)s), 25832)
            AS geom, %(start_floor)s as floor_id),
    """, {
        "start_x": point[0],
        "start_y": point[1],
        "start_floor": floor
    }


def get_parameterised_routing_sql(start_location, queryResult):
    parameter_list = {}
    start_location_sql, start_location_params = get_start_location(start_location)
    parameter_list.update(start_location_params)
    destinations_sql, destinations_params = get_destinations(queryResult)
    parameter_list.update(destinations_params)

    # acessibility_bool = queryResult.accessibility
    # accessibility_sql, accessibility_params = get_acessibility(acessibility_bool)

    return """
        DROP TABLE IF EXISTS all_lines;
        CREATE TABLE all_lines AS
        WITH """ + destinations_sql +"""

            target_points AS (
            SELECT t.transition_point_id AS id,
            t.geom, t.floor_id FROM transition_point t
            JOIN specific_room s ON ST_Intersects(t.geom,s.geom)
            WHERE t.floor_id=s.floor_id),
        
        
            lines AS (
            SELECT indoor_space_id AS id,
            ST_ApproximateMedialAxis(geom) AS geom,
            floor_id as floor_id FROM indoor_space 
            WHERE space_type = 'corridor' or space_type = 'common_area'),
        

            spatial_join_point_area_trans AS (
            Select transition_point_id AS id,
            (ST_Dump(transition_point.geom)).geom AS geom,
            transition_point.floor_id AS floor_id,
            transition_area_id AS transition_area_id, c.id AS indoor_space_id
        
        
            FROM transition_point JOIN transition_area 
            ON ST_Intersects(transition_point.geom, transition_area.geom)
            CROSS JOIN LATERAL (
                SELECT indoor_space_id AS id FROM indoor_space i
                WHERE ST_DWithin(i.geom, transition_point.geom, 1000) and
                i.floor_id=transition_point.floor_id
                ORDER BY ST_Distance(i.geom, transition_point.geom)
            LIMIT 1 ) c
        ),
        
        
            line_in_trans_area AS (
            SELECT s.transition_area_id AS id,
            ST_MakeLine(s.geom, t.geom) AS geom, s.floor_id as floor_id
            FROM spatial_join_point_area_trans s
            JOIN spatial_join_point_area_trans t
            ON s.transition_area_id = t.transition_area_id and s.floor_id=t.floor_id
            WHERE s.id < t.id),
        
                
            nearest_line AS (
            SELECT p.id, l.geom, p.floor_id AS floor_id
            FROM target_points p
            CROSS JOIN LATERAL (
                SELECT geom FROM
                lines l WHERE ST_DWithin(l.geom, p.geom, 1000)
                and p.floor_id=l.floor_id
                ORDER BY ST_Distance(l.geom, p.geom)
                LIMIT 1 )
            l),

        
            lines_to_line AS (
            Select p.id AS id, ST_ShortestLine(p.geom, n.geom) AS geom,
            p.floor_id AS floor_id
            FROM target_points p
            JOIN nearest_line n ON p.id=n.id
            ),


            points_walking_areas AS (
            SELECT p.transition_point_id AS id,
            p.geom AS geom,  p.floor_id AS floor_id
            FROM transition_point p JOIN indoor_space i
            ON ST_Intersects(p.geom, i.geom) 
            WHERE (i.space_type = 'corridor' or i.space_type = 'common_area'
            or i.space_type = 'exit_area') 
            and  p.transition_point_id not in (SELECT id FROM spatial_join_point_area_trans)
            and p.floor_id=i.floor_id),


            get_ids AS (
            SELECT c.id AS closet_id, s.id AS second_id, p.id AS point_id,
            p.geom AS geom, p.floor_id AS floor_id
            FROM points_walking_areas p
            CROSS JOIN LATERAL (
                SELECT indoor_space_id AS id
                FROM indoor_space i
                WHERE ST_DWithin(i.geom, p.geom, 1000) AND p.floor_id=i.floor_id
                ORDER BY ST_Distance(i.geom, p.geom)
                LIMIT 1
            ) c
            CROSS JOIN LATERAL (
                SELECT indoor_space_id as id FROM indoor_space i 
                WHERE ST_DWithin(i.geom, p.geom, 1000) AND p.floor_id=i.floor_id
                ORDER BY ST_Distance(i.geom, p.geom)
                OFFSET 1 LIMIT 1
            ) s),


            lines_trans_lines AS (
            SELECT p.point_id AS id,
            ST_MakeLine(
                ARRAY[ST_ClosestPoint(s.geom, p.geom),p.geom,ST_ClosestPoint(t.geom, p.geom)]) 
            AS geom, p.floor_id AS floor_id
            FROM get_ids p
            JOIN lines s ON p.closet_id =s.id
            JOIN lines t ON p.second_id=t.id),


            lines_trans_area_lines AS (
                SELECT
                    p.id,
                    ST_MakeLine(
                        p.geom,
                        ST_ClosestPoint(s.geom, p.geom)
                    ) AS geom,
                    p.floor_id
                        FROM spatial_join_point_area_trans p
                        JOIN lines s
                            ON p.indoor_space_id = s.id),""" + start_location_sql + """

            start_route AS (
            SELECT 0 AS id,
            ST_MakeLine(ARRAY[s.geom,p.geom,ST_ClosestPoint(t.geom, p.geom)])
            AS geom, s.floor_id 
            FROM start_location s
            JOIN indoor_space
            ON ST_Intersects(s.geom, indoor_space.geom)
            AND s.floor_id=indoor_space.floor_id
            JOIN transition_point p ON ST_Intersects(indoor_space.geom, p.geom)
            AND indoor_space.floor_id=p.floor_id 
            CROSS JOIN LATERAL (
                SELECT indoor_space_id as id
                FROM indoor_space i
                WHERE ST_DWithin(i.geom, p.geom, 1000)
                and (i.space_type = 'corridor' or i.space_type = 'common_area')
                and i.floor_id=s.floor_id
                ORDER BY ST_Distance(i.geom, p.geom) LIMIT 1
            ) i
            join lines t on t.id = i.id),

            
        all_lines AS (
            SELECT id,  geom, floor_id FROM lines
            union all select id, geom, floor_id from lines_to_line
            union all select id, geom, floor_id from line_in_trans_area
            union all select id, geom, floor_id from lines_trans_lines
            union all select id, geom, floor_id from lines_trans_area_lines
            union all select id, geom, floor_id from start_route
        )
        SELECT * FROM all_lines;


        -- The following is to everything ready for pgRouting. We split multilinestring geometries into linestring. 

        DROP TABLE IF EXISTS routing_table;
        CREATE TABLE routing_table AS
        WITH ww_selected AS (
            SELECT
                id AS original_id,
                floor_id,
                ST_LineMerge(geom) AS geom
            FROM all_lines
        ),

        ww_extra_cleanup AS (
            SELECT
                original_id,
                floor_id,
                (ST_Dump(geom)).geom AS geom
            FROM ww_selected
            WHERE ST_GeometryType(geom) = 'ST_MultiLineString'
        ),

        combined AS (
            SELECT
                original_id,
                floor_id,
                geom
            FROM ww_selected
            WHERE ST_GeometryType(geom) != 'ST_MultiLineString'

            UNION ALL

            SELECT
                original_id,
                floor_id,
                geom
            FROM ww_extra_cleanup
            WHERE ST_GeometryType(geom) != 'ST_MultiLineString'
        )

        SELECT
            ROW_NUMBER() OVER () AS id,
            original_id,
            geom,
            floor_id
        FROM combined
        WHERE geom IS NOT NULL;

        -- The following creates the structure and data needed for routing.
        -- First, creates a node network


        --DROP TABLE IF EXISTS routing_table_noded CASCADE;
        --SELECT pgr_nodenetwork('routing_table', 1, 'id', 'geom');
        -- this is the new version
        DROP TABLE IF EXISTS routing_table_noded CASCADE;

        CREATE TABLE routing_table_noded (
            id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            old_id bigint NOT NULL,
            sub_id integer NOT NULL,
            floor_id bigint NOT NULL,
            geom geometry NOT NULL,
            source bigint,
            target bigint
        );

        -- Ensure the IDs are indexed before running pgr_nodeNetwork
        CREATE INDEX IF NOT EXISTS routing_table_id_idx
            ON indoor_navigation.routing_table (id);

        --Ensures the geom is stored before pgr_nodeNetwork
        CREATE INDEX IF NOT EXISTS routing_table_geom_gidx
            ON indoor_navigation.routing_table USING GIST (geom);

        DO $$
        DECLARE
            -- A value of same type as floor_id
            current_floor_id routing_table.floor_id%%TYPE;
        BEGIN
            FOR current_floor_id IN
                SELECT DISTINCT floor_id
                FROM routing_table
                ORDER BY floor_id
            LOOP
                PERFORM pgr_nodeNetwork(
                    'routing_table',
                    1,
                    id => 'id',
                    the_geom => 'geom',
                    table_ending => 'noding_work',
                    rows_where => 'floor_id = ' || current_floor_id,
                    outall => true
                );
                --apends the data into routing_table_noded
                INSERT INTO routing_table_noded (old_id, sub_id, floor_id, geom)
                SELECT n.old_id, n.sub_id, r.floor_id, n.geom
                FROM routing_table_noding_work AS n
                JOIN routing_table AS r ON r.id = n.old_id
                WHERE r.floor_id = current_floor_id;
            END LOOP;
        END;
        $$;

        -- Establish route costs

        ALTER TABLE routing_table_noded
            ADD cost NUMERIC
            GENERATED ALWAYS AS (
                ST_Length(geom)
            )
            STORED;

        ALTER TABLE routing_table_noded
            ADD reverse_cost NUMERIC NOT NULL DEFAULT -1;

        UPDATE routing_table_noded
        SET reverse_cost = cost;

        SELECT pgr_createTopology('routing_table_noded',0.01,'geom','id');
        SELECT pgr_analyzeGraph('routing_table_noded',0.01,'geom','id');

        -- Create route with search algorithm

        WITH """ + destinations_sql + """

        target_points AS (
            SELECT t.transition_point_id AS id,
            t.geom, t.floor_id FROM transition_point t
            JOIN specific_room s ON ST_Intersects(t.geom,s.geom)
            WHERE t.floor_id=s.floor_id),
        
        """ + start_location_sql + """

        spatial_join_start_loc_node AS (
            SELECT v.id AS node_id, s.floor_id
            FROM routing_table_noded_vertices_pgr v
            JOIN start_location s ON ST_Equals(v.the_geom, s.geom)
        ),
        -- Target node, holds the node id for target (for each target)
        spatial_join_target_loc_node AS (
            SELECT t.geom, v.id AS node_id, t.floor_id FROM routing_table_noded_vertices_pgr v
            JOIN target_points t ON ST_Equals(v.the_geom,t.geom)
        ),
        routes as (select d.*, geom, (SELECT floor_id FROM spatial_join_start_loc_node) as floor_id
        FROM (
                SELECT array_agg(DISTINCT t.node_id) AS node_ids
                FROM spatial_join_target_loc_node AS t
                WHERE t.floor_id = (
                    SELECT s.floor_id FROM spatial_join_start_loc_node AS s
                )
                HAVING count(*) > 0
            ) AS targets
            CROSS JOIN LATERAL pgr_dijkstra(
                'SELECT
                rn.id,
                rn.source,
                rn.target,
                rn.cost,
                rn.reverse_cost
                FROM routing_table_noded rn
                WHERE source IS NOT NULL AND target IS NOT NULL 
                AND rn.floor_id ='|| (SELECT floor_id FROM spatial_join_start_loc_node),
                (SELECT s.node_id FROM spatial_join_start_loc_node s),
                (ARRAY(SELECT node_id FROM spatial_join_target_loc_node t
                    WHERE t.floor_id = (
                        SELECT s.floor_id FROM spatial_join_start_loc_node AS s
                ))),
                TRUE
            ) d
            INNER JOIN routing_table_noded x ON d.edge = x.id),

            shortest_path as (
            SELECT
                end_vid,
                SUM(cost) AS total_cost
            FROM routes
            WHERE edge <> -1
            GROUP BY end_vid
            ORDER by total_cost
            Limit 1
            ),
            shortest_path_geom as (
            select s.*, r.total_cost, FALSE AS using_transition_area from routes s join shortest_path r 
            on s.end_vid=r.end_vid ),
            


            spatial_join_point_area_trans AS (
            Select transition_point_id AS id,
            (ST_Dump(transition_point.geom)).geom AS geom,
            transition_point.floor_id AS floor_id,
            transition_area_id AS transition_area_id, c.id AS indoor_space_id
            FROM transition_point JOIN transition_area 
            ON ST_Intersects(transition_point.geom, transition_area.geom)
            CROSS JOIN LATERAL (
                SELECT indoor_space_id AS id FROM indoor_space i
                WHERE ST_DWithin(i.geom, transition_point.geom, 1000) and
                i.floor_id=transition_point.floor_id
                ORDER BY ST_Distance(i.geom, transition_point.geom)
            LIMIT 1 ) c),
            
            
            find_trans_area_points_same_floor AS (
                SELECT DISTINCT
                    ta.transition_area_id,
                    tp.transition_point_id,
                    tp.floor_id,
                    v.id AS node_id,
                    v.the_geom AS node_geom,
                    tp.geom AS transition_point_geom
                FROM transition_point tp
                JOIN transition_area ta
                    ON ST_Intersects(tp.geom, ta.geom)
                JOIN LATERAL (
                    SELECT v.id, v.the_geom
                    FROM routing_table_noded_vertices_pgr v
                    WHERE ST_DWithin(v.the_geom, tp.geom, 1)
                    ORDER BY ST_Distance(v.the_geom, tp.geom)
                    LIMIT 1
                ) v ON TRUE
                WHERE tp.floor_id = (
                    SELECT floor_id
                    FROM start_location
                )
            ),
            
            routes_to_transition_area AS (
                SELECT
                    d.*,
                    c.transition_area_id,
                    c.transition_point_id,
                    x.geom,
                    c.floor_id
                FROM pgr_dijkstra(
                    'SELECT
                        rn.id,
                        rn.source,
                        rn.target,
                        rn.cost,
                        rn.reverse_cost
                    FROM routing_table_noded rn
                    WHERE rn.source IS NOT NULL
                    AND rn.target IS NOT NULL
                    AND rn.floor_id = ' ||
                (SELECT floor_id FROM start_location),
                    (SELECT node_id
                    FROM spatial_join_start_loc_node),
                    (ARRAY(
                        SELECT DISTINCT node_id
                        FROM find_trans_area_points_same_floor
                    )),
                    TRUE
                ) d
                inner JOIN routing_table_noded x
                    ON d.edge = x.id
                JOIN find_trans_area_points_same_floor c
                    ON d.end_vid = c.node_id
            ),
            -- shortest path from source to nearest transition area (does not add additonal cost for transition area)
            shortest_path_transition_area as (
                SELECT
                    end_vid,
                    SUM(cost) AS total_cost
                FROM routes_to_transition_area
                WHERE edge <> -1
                GROUP BY end_vid
                ORDER by total_cost
                Limit 1
                ),

            shortest_path_transition_area_geom as (
            select r.*, s.total_cost from routes_to_transition_area r join shortest_path_transition_area s
            on r.end_vid=s.end_vid ),

            routes_from_transition_area AS (
                SELECT
                    d.*,
                    p.start_node AS start_vid,
                    x.geom,
                    t.floor_id
                    FROM (
                        SELECT
                            (
                                SELECT DISTINCT v.id
                                FROM shortest_path_transition_area_geom s
                                JOIN transition_area ta
                                    ON s.transition_area_id = ta.transition_area_id
                                JOIN transition_point tp
                                    ON ST_Intersects(tp.geom, ta.geom)
                                CROSS JOIN LATERAL (
                                    SELECT v.id
                                    FROM routing_table_noded_vertices_pgr v
                                    ORDER BY v.the_geom <-> tp.geom
                                    LIMIT 1
                                ) v
                                WHERE tp.floor_id = (
                                    SELECT DISTINCT floor_id
                                    FROM spatial_join_target_loc_node
                                )
                                LIMIT 1
                            ) AS start_node,
                
                            (
                                ARRAY(SELECT node_id
                                FROM spatial_join_target_loc_node)
                            ) AS target_node,
                
                            (
                                SELECT DISTINCT floor_id
                                FROM spatial_join_target_loc_node
                            ) AS floor_id
                    ) p
                
                    CROSS JOIN LATERAL pgr_dijkstra(
                        'SELECT
                            rn.id,
                            rn.source,
                            rn.target,
                            rn.cost,
                            rn.reverse_cost
                        FROM routing_table_noded rn
                        WHERE rn.source IS NOT NULL
                        AND rn.target IS NOT NULL
                        AND rn.floor_id = ' || p.floor_id,
                
                        p.start_node,
                        p.target_node,
                        TRUE
                    ) d
                
                    INNER JOIN routing_table_noded x
                        ON d.edge = x.id
                
                    JOIN spatial_join_target_loc_node t
                        ON t.node_id = d.end_vid
            ),
            
        -- shortest path from transtion area to target. Adds additional cost of 10 for using elevatior/stairs
            shortest_path_from_transition_area as (
                SELECT
                    end_vid,
                    SUM(cost) +10 AS total_cost
                FROM routes_from_transition_area
                WHERE edge <> -1
                GROUP BY end_vid
                ORDER by total_cost
                Limit 1
                ),

            shortest_path_from_transition_area_geom as (
                select r.*, s.total_cost from routes_from_transition_area r join shortest_path_from_transition_area s
                on r.end_vid=s.end_vid ),

        shortest_path_multiple_floors as ( 
            SELECT 
            seq,
            path_seq, 
            node, 
            edge,
            cost, (
            (SELECT total_cost FROM shortest_path_transition_area ORDER BY path_seq LIMIT 1) 
            + (SELECT total_cost FROM shortest_path_from_transition_area ORDER BY path_seq LIMIT 1)

            ) AS total_cost,
            end_vid, 
            geom, 
            floor_id,
            TRUE AS using_transition_area
            FROM (
                select  seq,path_seq, node, edge,cost, total_cost, end_vid, geom, floor_id from shortest_path_transition_area_geom
                union all select  seq,path_seq, node, edge,cost, total_cost, end_vid, geom, floor_id from shortest_path_from_transition_area_geom)),




        -- Holds the route for same floor shortest path and the (two) paths for the shortest route for multiple floors
        both_routes as (
            select 
                seq,
                path_seq, 
                node, 
                edge,
                cost, 
                total_cost, 
                end_vid, 
                geom, 
                floor_id, 
                using_transition_area 
                from shortest_path_geom 
            union all
            select 
                seq,
                path_seq, 
                node, 
                edge,
                cost, 
                total_cost, 
                end_vid, 
                geom, 
                floor_id, 
                using_transition_area 
                from shortest_path_multiple_floors
                ),

        -- finds the shortest path by comparing both same floor shortest path and multiple floors shortest path
        final_route as (
            SELECT
                using_transition_area,
                total_cost
            FROM both_routes
            GROUP BY using_transition_area, total_cost
            ORDER BY total_cost 
            LIMIT 1
        ),

        -- The geom of the room where we start
        start_room_geom as(
            SELECT
                i.geom,
                i.floor_id        
            FROM start_location s JOIN indoor_space i ON ST_Intersects(s.geom, i.geom) WHERE s.floor_id = i.floor_id
        ),

        -- The geom of the target room (only the final one)
        -- RIGHT JOIN is to ensure we have the correct end_vid of the final target
        target_room_geom as(
            SELECT 
            i.geom,
            i.floor_id    
            FROM spatial_join_target_loc_node tn 
            RIGHT JOIN (
                SELECT
                    b.end_vid
                FROM both_routes b 
                JOIN final_route f ON b.using_transition_area=f.using_transition_area 
                GROUP BY b.end_vid
            ) s ON tn.node_id = s.end_vid
            JOIN indoor_space i ON ST_Intersects(tn.geom,i.geom) WHERE tn.floor_id = i.floor_id
        )

        SELECT ST_AsGeoJSON(b.geom)::json, floor_id FROM both_routes b JOIN final_route f ON b.using_transition_area=f.using_transition_area
            UNION ALL SELECT ST_AsGeoJSON(geom)::json, floor_id FROM start_room_geom
            UNION ALL SELECT ST_AsGeoJSON(geom)::json, floor_id FROM target_room_geom;
        --   select geom, floor_id, total_cost from (select * from shortest_path_multiple_floors 
        --           union all select * from shortest_path_geom) where floor_id=2
                -- union all select geom, floor_id, NULL as total_cost from indoor_navigation.indoor_space where floor_id=2
                -- union all select geom, 0 as floor_id,  NULL as total_cost from indoor_navigation.transition_area;
        """, parameter_list