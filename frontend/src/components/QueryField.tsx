import type { PointOnRoute } from "../../types"

interface QueryFieldProps {
  startLocation: PointOnRoute
  onFindRoute: (query: string, startLocation: PointOnRoute) => void | Promise<void>
}

export default function QueryField({
  startLocation,
  onFindRoute,
}: QueryFieldProps) {
    async function handleRouteSubmit(formData: FormData) {
        const value = formData.get('query')
        const query = typeof value === 'string' ? value.trim() : ''

        if (query) {
        await onFindRoute(query, startLocation)
        }
    }
    return (
        <form className="mt-4 flex items-end gap-2" action={handleRouteSubmit}>
            <label className="block min-w-0 flex-1">
                <span className="mb-2 block">Where do you want to go?</span>
                <input
                name="query"
                placeholder="Where’s the nearest toilet?"
                className="min-h-11 w-full rounded-lg border border-gray-300 px-3"
                required
                />
            </label>

            <button
                type="submit"
                className="min-h-11 shrink-0 rounded-lg bg-gray-900 px-3 text-white"
            >
                Find route
            </button>
        </form>
        )
    }