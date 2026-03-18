<script lang="ts" module>
	// Coffee-themed SVG icons as reusable snippets
</script>

<script lang="ts">
	let { icon, size = 24, className = '' }: {
		icon: 'bean' | 'grinder' | 'cup' | 'star' | 'settings' | 'search' | 'plus' | 'back' | 'delete' | 'link' | 'chevron' | 'users';
		size?: number;
		className?: string;
	} = $props();
</script>

<svg viewBox="0 0 24 24" width={size} height={size} class={className} fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
	{#if icon === 'bean'}
		<ellipse cx="12" cy="12" rx="5" ry="8" transform="rotate(-30 12 12)" />
		<path d="M9.5 7c1 2.5 1 5 0 10" />
	{:else if icon === 'grinder'}
		<rect x="7" y="12" width="10" height="8" rx="1" />
		<path d="M9 12V9a3 3 0 0 1 6 0v3" />
		<circle cx="12" cy="16" r="1.5" />
		<path d="M12 6V4" />
		<path d="M10 4h4" />
	{:else if icon === 'cup'}
		<path d="M5 8h12a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2h-1" />
		<path d="M5 8v8a3 3 0 0 0 3 3h4a3 3 0 0 0 3-3V8" />
		<path d="M5 8h10" />
		<path d="M8 5c0-1 .5-2 1.5-2s1.5 1 1.5 2" />
	{:else if icon === 'star'}
		<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" fill="currentColor" stroke="none" />
	{:else if icon === 'settings'}
		<circle cx="12" cy="12" r="3" />
		<path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83" />
	{:else if icon === 'search'}
		<circle cx="11" cy="11" r="7" />
		<path d="M21 21l-4.35-4.35" />
	{:else if icon === 'plus'}
		<path d="M12 5v14M5 12h14" />
	{:else if icon === 'back'}
		<path d="M19 12H5M12 19l-7-7 7-7" />
	{:else if icon === 'delete'}
		<path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
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
