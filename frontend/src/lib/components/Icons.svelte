<script lang="ts" module>
	// Coffee-themed SVG icons as reusable snippets
</script>

<script lang="ts">
	let { icon, size = 24, className = '' }: {
		icon: 'search' | 'plus' | 'back' | 'link' | 'chevron' | 'users';
		size?: number;
		className?: string;
	} = $props();
</script>

<svg viewBox="0 0 24 24" width={size} height={size} class={className} fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
	{#if icon === 'search'}
		<circle cx="11" cy="11" r="7" />
		<path d="M21 21l-4.35-4.35" />
	{:else if icon === 'plus'}
		<path d="M12 5v14M5 12h14" />
	{:else if icon === 'back'}
		<path d="M19 12H5M12 19l-7-7 7-7" />
	{:else if icon === 'link'}
		<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
		<path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
	{:else if icon === 'chevron'}
		<path d="M6 9l6 6 6-6" />
	{:else if icon === 'users'}
		<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
		<circle cx="9" cy="7" r="4" />
		<path d="M23 21v-2a4 4 0 0 0-3-3.87" />
		<path d="M16 3.13a4 4 0 0 1 0 7.75" />
	{/if}
</svg>
