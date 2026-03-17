import { writable } from 'svelte/store';

export type Lang = 'en' | 'uk';

const stored = typeof localStorage !== 'undefined'
	? (localStorage.getItem('beanbrain-lang') as Lang) || 'en'
	: 'en';

export const lang = writable<Lang>(stored);

lang.subscribe((value) => {
	if (typeof localStorage !== 'undefined') {
		localStorage.setItem('beanbrain-lang', value);
	}
});
