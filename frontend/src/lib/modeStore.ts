import { writable } from 'svelte/store';

export type AppMode = 'my-coffee' | 'discover';

const STORAGE_KEY = 'beanbrain-mode';

function createModeStore() {
	const initial: AppMode =
		typeof window !== 'undefined'
			? (localStorage.getItem(STORAGE_KEY) as AppMode) ?? 'my-coffee'
			: 'my-coffee';

	const store = writable<AppMode>(initial);

	store.subscribe(v => {
		if (typeof window !== 'undefined') {
			localStorage.setItem(STORAGE_KEY, v);
		}
	});

	return store;
}

export const appMode = createModeStore();
