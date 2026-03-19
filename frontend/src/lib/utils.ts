export function toggleId(arr: number[], id: number): number[] {
	return arr.includes(id) ? arr.filter(d => d !== id) : [...arr, id];
}
