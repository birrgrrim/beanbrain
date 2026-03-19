import { writable } from 'svelte/store';

const isBrowser = typeof window !== 'undefined';
const stored = isBrowser
	? localStorage.getItem('beanbrain-person')
	: null;

export const activePerson = writable<number | null>(stored ? parseInt(stored, 10) : null);

activePerson.subscribe((value) => {
	if (isBrowser) {
		if (value !== null) {
			localStorage.setItem('beanbrain-person', String(value));
		} else {
			localStorage.removeItem('beanbrain-person');
		}
	}
});
