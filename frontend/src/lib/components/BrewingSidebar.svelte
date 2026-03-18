<script lang="ts">
	import type { BrewSetup } from '$lib/api';
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';

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

<aside class="w-[420px] flex-shrink-0 bg-card border-r border-stone-200 flex flex-col">
	<div class="p-4 border-b border-stone-100">
		<div class="relative">
			<Icons icon="search" size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-300" />
			<input
				type="text"
				bind:value={search}
				placeholder={$t('brewing.search')}
				class="w-full pl-9 pr-4 py-2.5 rounded-lg border border-stone-200 bg-card-inset text-base
					focus:outline-none focus:ring-2 focus:ring-amber-400/50 focus:border-amber-300
					placeholder:text-stone-400"
			/>
		</div>
	</div>

	<div class="flex-1 overflow-y-auto">
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

		{#if brewSetups.length === 0}
			<div class="p-6 text-center">
				<img src="/img/select-brewing.png" alt="" class="mx-auto mb-3 opacity-60" style="max-width: 140px;" />
				<p class="text-sm text-stone-500">{$t('brewing.empty')}</p>
				<p class="text-xs text-stone-400 mt-1">{$t('brewing.empty_hint')}</p>
			</div>
		{:else if filtered.length === 0}
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
	</div>
</aside>
