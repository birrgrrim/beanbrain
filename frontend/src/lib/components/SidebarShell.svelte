<script lang="ts">
	import Icons from './Icons.svelte';
	import type { Snippet } from 'svelte';

	let {
		searchPlaceholder,
		search = $bindable(),
		children,
	}: {
		searchPlaceholder: string;
		search: string;
		children: Snippet;
	} = $props();
</script>

<aside class="w-[420px] flex-shrink-0 bg-card border-r border-stone-200 flex flex-col">
	<div class="p-4 border-b border-stone-100">
		<div class="relative">
			<Icons icon="search" size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-300" />
			<input
				type="text"
				bind:value={search}
				placeholder={searchPlaceholder}
				class="w-full pl-9 pr-4 py-2.5 rounded-lg border border-stone-200 bg-card-inset text-base
					focus:outline-none focus:ring-2 focus:ring-amber-400/50 focus:border-amber-300
					placeholder:text-stone-400"
			/>
		</div>
	</div>

	<div class="flex-1 overflow-y-auto">
		{@render children()}
	</div>
</aside>
