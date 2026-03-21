import { writable } from 'svelte/store';

const isBrowser = typeof window !== 'undefined';

function persistentStore(key: string) {
	const stored = isBrowser ? localStorage.getItem(key) : null;
	const store = writable<number | null>(stored ? parseInt(stored, 10) : null);

	store.subscribe((value) => {
		if (isBrowser) {
			if (value !== null) {
				localStorage.setItem(key, String(value));
			} else {
				localStorage.removeItem(key);
			}
		}
	});

	return store;
}

export const activeGrinder = persistentStore('beanbrain-grinder');
export const activeBrewSetup = persistentStore('beanbrain-brew-setup');
