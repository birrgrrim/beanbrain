import { writable } from 'svelte/store';

const stored = typeof localStorage !== 'undefined'
	? localStorage.getItem('beanbrain-person')
	: null;

export const activePerson = writable<number | null>(stored ? parseInt(stored, 10) : null);

activePerson.subscribe((value) => {
	if (typeof localStorage !== 'undefined') {
		if (value !== null) {
			localStorage.setItem('beanbrain-person', String(value));
		} else {
			localStorage.removeItem('beanbrain-person');
		}
	}
});
