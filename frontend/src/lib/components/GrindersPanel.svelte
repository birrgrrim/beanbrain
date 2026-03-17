<script lang="ts">
	import { api, type Equipment, type BrewMethod, type BasketSize } from '$lib/api';
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';

	let equipmentList = $state<Equipment[]>([]);
	let brewMethods = $state<BrewMethod[]>([]);
	let basketSizes = $state<BasketSize[]>([]);

	async function load() {
		const [eq, bm, bs] = await Promise.all([
			api.equipment.list(),
			api.equipment.brewMethods(),
			api.equipment.basketSizes(),
		]);
		equipmentList = eq;
		brewMethods = bm;
		basketSizes = bs;
	}

	$effect(() => { load(); });

	const grinders = $derived(equipmentList.filter(e => e.type === 'grinder'));
	const machines = $derived(equipmentList.filter(e => e.type === 'machine'));
</script>

<div class="max-w-lg mx-auto p-6 space-y-6">
	<h2 class="text-2xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
		{$t('grinders.title')}
	</h2>

	<!-- Grinders -->
	<div class="bg-white rounded-2xl border border-stone-100 shadow-sm p-5">
		<div class="flex items-center gap-2 mb-4">
			<Icons icon="grinder" size={18} className="text-stone-400" />
			<h3 class="font-semibold text-stone-700">{$t('grinders.grinders')}</h3>
		</div>
		{#if grinders.length === 0}
			<p class="text-sm text-stone-300">No grinders configured</p>
		{:else}
			{#each grinders as g}
				<div class="flex items-center gap-3 py-2.5 px-3 rounded-lg hover:bg-stone-50 transition-colors">
					<Icons icon="grinder" size={20} className="text-amber-600" />
					<div>
						<p class="text-sm font-medium text-stone-700">{g.name}</p>
						{#if g.model}<p class="text-xs text-stone-300">{g.model}</p>{/if}
					</div>
				</div>
			{/each}
		{/if}
	</div>

	<!-- Machines -->
	<div class="bg-white rounded-2xl border border-stone-100 shadow-sm p-5">
		<div class="flex items-center gap-2 mb-4">
			<Icons icon="cup" size={18} className="text-stone-400" />
			<h3 class="font-semibold text-stone-700">{$t('grinders.machines')}</h3>
		</div>
		{#if machines.length === 0}
			<p class="text-sm text-stone-300">No machines configured</p>
		{:else}
			{#each machines as m}
				<div class="flex items-center gap-3 py-2.5 px-3 rounded-lg hover:bg-stone-50 transition-colors">
					<Icons icon="cup" size={20} className="text-amber-600" />
					<div>
						<p class="text-sm font-medium text-stone-700">{m.name}</p>
						{#if m.model}<p class="text-xs text-stone-300">{m.model}</p>{/if}
					</div>
				</div>
			{/each}
		{/if}
	</div>

	<!-- Brew Methods -->
	<div class="bg-white rounded-2xl border border-stone-100 shadow-sm p-5">
		<div class="flex items-center gap-2 mb-4">
			<Icons icon="bean" size={18} className="text-stone-400" />
			<h3 class="font-semibold text-stone-700">{$t('grinders.brew_methods')}</h3>
		</div>
		<div class="flex flex-wrap gap-2">
			{#each brewMethods as m}
				<span class="px-3 py-1.5 bg-stone-50 rounded-lg text-sm text-stone-600">{m.name}</span>
			{/each}
		</div>
	</div>

	<!-- Basket Sizes -->
	<div class="bg-white rounded-2xl border border-stone-100 shadow-sm p-5">
		<div class="flex items-center gap-2 mb-4">
			<Icons icon="settings" size={18} className="text-stone-400" />
			<h3 class="font-semibold text-stone-700">{$t('grinders.baskets')}</h3>
		</div>
		<div class="flex gap-3">
			{#each basketSizes as bs}
				<div class="px-5 py-3 bg-stone-50 rounded-xl text-center">
					<p class="text-xl font-bold text-stone-600">{bs.size_grams}<span class="text-sm font-normal text-stone-400">g</span></p>
				</div>
			{/each}
		</div>
	</div>
</div>
