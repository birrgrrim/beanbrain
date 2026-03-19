import { writable } from 'svelte/store';

export type Lang = 'en' | 'uk';

const isBrowser = typeof window !== 'undefined';
const stored = isBrowser
	? (localStorage.getItem('beanbrain-lang') as Lang) || 'en'
	: 'en';

export const lang = writable<Lang>(stored);

lang.subscribe((value) => {
	if (isBrowser) {
		localStorage.setItem('beanbrain-lang', value);
	}
});
