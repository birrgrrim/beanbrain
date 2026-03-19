<script lang="ts">
	import type { Roastery } from '$lib/api';
	import { t } from '$lib/i18n';
	import SidebarShell from './SidebarShell.svelte';

	let { roasteries = [], selectedId = null, onSelect, onAdd }: {
		roasteries: Roastery[];
		selectedId: number | null;
		onSelect: (id: number) => void;
		onAdd: () => void;
	} = $props();

	let search = $state('');
	let filtered = $derived(
		search.trim()
			? roasteries.filter(r =>
				r.name.toLowerCase().includes(search.toLowerCase())
			)
			: roasteries
	);
</script>

<SidebarShell searchPlaceholder={$t('roastery.search')} bind:search>
	<!-- Add roastery card -->
	<button
		onclick={onAdd}
		class="w-full text-left px-5 py-3 border-b border-stone-50 transition-colors
			hover:bg-amber-50/50 group"
	>
		<div class="flex items-center gap-3">
			<img src="/img/add-roastery.png" alt="" class="w-20 h-20 opacity-50 group-hover:opacity-70 transition-opacity" />
			<p class="text-base font-medium text-amber-600 group-hover:text-amber-700">{$t('roastery.add')}</p>
		</div>
	</button>

	{#if filtered.length === 0 && search}
		<div class="p-6 text-center">
			<p class="text-sm text-stone-500">{$t('sidebar.no_matches')}</p>
		</div>
	{:else}
		{#each filtered as roastery}
			<button
				onclick={() => onSelect(roastery.id)}
				class="w-full text-left px-5 py-4 border-b border-stone-50 transition-colors
					hover:bg-amber-50/50
					{selectedId === roastery.id ? 'bg-amber-50 border-l-2 border-l-amber-600' : ''}"
			>
				<div class="flex items-center gap-3">
					<img src="/img/roastery.png" alt="" class="w-20 h-20 opacity-60" />
					<div class="min-w-0 flex-1">
						<p class="font-semibold text-lg text-stone-800 truncate">{roastery.name}</p>
						{#if roastery.website}
							<p class="text-sm text-stone-400 truncate">{roastery.website}</p>
						{/if}
					</div>
				</div>
			</button>
		{/each}
	{/if}
</SidebarShell>
