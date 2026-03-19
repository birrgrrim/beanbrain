<script lang="ts">
	import type { BrewSetup } from '$lib/api';
	import { t } from '$lib/i18n';
	import SidebarShell from './SidebarShell.svelte';

	let { brewSetups = [], selectedId = null, onSelect, onAdd }: {
		brewSetups: BrewSetup[];
		selectedId: number | null;
		onSelect: (id: number) => void;
		onAdd: () => void;
	} = $props();

	let search = $state('');
	let filtered = $derived(
		search.trim()
			? brewSetups.filter(s =>
				s.name.toLowerCase().includes(search.toLowerCase()) ||
				s.method_type.toLowerCase().includes(search.toLowerCase())
			)
			: brewSetups
	);
</script>

<SidebarShell searchPlaceholder={$t('brewing.search')} bind:search>
	<!-- Add brew setup card -->
	<button
		onclick={onAdd}
		class="w-full text-left px-5 py-3 border-b border-stone-50 transition-colors
			hover:bg-amber-50/50 group"
	>
		<div class="flex items-center gap-3">
			<img src="/img/add-brewing.png" alt="" class="w-20 h-20 opacity-50 group-hover:opacity-70 transition-opacity" />
			<p class="text-base font-medium text-amber-600 group-hover:text-amber-700">{$t('brewing.add')}</p>
		</div>
	</button>

	{#if filtered.length === 0 && search}
		<div class="p-6 text-center">
			<p class="text-sm text-stone-500">{$t('sidebar.no_matches')}</p>
		</div>
	{:else}
		{#each filtered as setup}
			<button
				onclick={() => onSelect(setup.id)}
				class="w-full text-left px-5 py-4 border-b border-stone-50 transition-colors
					hover:bg-amber-50/50
					{selectedId === setup.id ? 'bg-amber-50 border-l-2 border-l-amber-600' : ''}"
			>
				<div class="flex items-center gap-3">
					<img src="/img/method-{setup.method_type}.png" alt="" class="w-20 h-20 opacity-60" />
					<div class="min-w-0 flex-1">
						<p class="font-semibold text-lg text-stone-800 truncate">{setup.name}</p>
						<div class="flex items-center gap-2 mt-0.5">
							<span class="text-sm text-stone-400">{$t(`method.${setup.method_type}`)}</span>
							{#if setup.basket_grams}
								<span class="text-stone-200">|</span>
								<span class="text-sm text-stone-400">{setup.basket_grams}g</span>
							{/if}
							{#if setup.is_default}
								<span class="text-xs bg-amber-100 text-amber-700 rounded-md px-2 py-0.5">{$t('common.default')}</span>
							{/if}
						</div>
					</div>
				</div>
			</button>
		{/each}
	{/if}
</SidebarShell>
