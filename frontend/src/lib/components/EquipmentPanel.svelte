<script lang="ts">
	import { api, type Equipment, type BrewMethod, type BasketSize, type Taster } from '$lib/api';
	import Icons from './Icons.svelte';

	let equipmentList = $state<Equipment[]>([]);
	let brewMethods = $state<BrewMethod[]>([]);
	let basketSizes = $state<BasketSize[]>([]);
	let tasters = $state<Taster[]>([]);

	let newTasterName = $state('');

	async function loadData() {
		const [eq, bm, bs, t] = await Promise.all([
			api.equipment.list(),
			api.equipment.brewMethods(),
			api.equipment.basketSizes(),
			api.tasters.list(),
		]);
		equipmentList = eq;
		brewMethods = bm;
		basketSizes = bs;
		tasters = t;
	}

	$effect(() => { loadData(); });

	async function addTaster() {
		if (!newTasterName.trim()) return;
		await api.tasters.create(newTasterName.trim());
		newTasterName = '';
		await loadData();
	}

	async function deleteTaster(id: number) {
		await api.tasters.delete(id);
		await loadData();
	}

	const grinders = $derived(equipmentList.filter(e => e.type === 'grinder'));
	const machines = $derived(equipmentList.filter(e => e.type === 'machine'));
</script>

<div class="max-w-2xl mx-auto p-6 space-y-8">
	<h2 class="text-2xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
		Settings
	</h2>

	<!-- Tasters -->
	<div class="bg-white rounded-2xl border border-stone-100 shadow-sm p-5">
		<div class="flex items-center gap-2 mb-4">
			<Icons icon="cup" size={18} className="text-stone-400" />
			<h3 class="font-semibold text-stone-700">Tasters</h3>
		</div>

		<div class="space-y-2 mb-3">
			{#each tasters as taster}
				<div class="flex items-center justify-between py-1.5">
					<span class="text-sm text-stone-700">{taster.name}</span>
					<button onclick={() => deleteTaster(taster.id)}
						class="p-1 text-stone-200 hover:text-red-400 transition-colors">
						<Icons icon="delete" size={14} />
					</button>
				</div>
			{/each}
			{#if tasters.length === 0}
				<p class="text-sm text-stone-300">No tasters yet</p>
			{/if}
		</div>

		<div class="flex gap-2">
			<input type="text" bind:value={newTasterName} placeholder="Add taster..."
				class="flex-1 px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
					focus:outline-none focus:ring-2 focus:ring-amber-400/50"
				onkeydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addTaster(); } }}
			/>
			<button onclick={addTaster} disabled={!newTasterName.trim()}
				class="px-4 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800
					transition-colors disabled:opacity-50 disabled:cursor-not-allowed">Add</button>
		</div>
	</div>

	<!-- Grinders -->
	<div class="bg-white rounded-2xl border border-stone-100 shadow-sm p-5">
		<div class="flex items-center gap-2 mb-4">
			<Icons icon="grinder" size={18} className="text-stone-400" />
			<h3 class="font-semibold text-stone-700">Grinders</h3>
		</div>
		{#each grinders as g}
			<div class="py-1.5">
				<span class="text-sm text-stone-700">{g.name}</span>
				{#if g.model}<span class="text-xs text-stone-300 ml-2">{g.model}</span>{/if}
			</div>
		{/each}
		{#if grinders.length === 0}
			<p class="text-sm text-stone-300">No grinders</p>
		{/if}
	</div>

	<!-- Machines -->
	<div class="bg-white rounded-2xl border border-stone-100 shadow-sm p-5">
		<div class="flex items-center gap-2 mb-4">
			<Icons icon="cup" size={18} className="text-stone-400" />
			<h3 class="font-semibold text-stone-700">Machines</h3>
		</div>
		{#each machines as m}
			<div class="py-1.5">
				<span class="text-sm text-stone-700">{m.name}</span>
				{#if m.model}<span class="text-xs text-stone-300 ml-2">{m.model}</span>{/if}
			</div>
		{/each}
		{#if machines.length === 0}
			<p class="text-sm text-stone-300">No machines</p>
		{/if}
	</div>

	<!-- Brew Methods -->
	<div class="bg-white rounded-2xl border border-stone-100 shadow-sm p-5">
		<div class="flex items-center gap-2 mb-4">
			<Icons icon="bean" size={18} className="text-stone-400" />
			<h3 class="font-semibold text-stone-700">Brew Methods</h3>
		</div>
		{#each brewMethods as m}
			<div class="py-1.5">
				<span class="text-sm text-stone-700">{m.name}</span>
			</div>
		{/each}
	</div>

	<!-- Basket Sizes -->
	<div class="bg-white rounded-2xl border border-stone-100 shadow-sm p-5">
		<div class="flex items-center gap-2 mb-4">
			<Icons icon="settings" size={18} className="text-stone-400" />
			<h3 class="font-semibold text-stone-700">Basket Sizes</h3>
		</div>
		<div class="flex gap-3">
			{#each basketSizes as bs}
				<div class="px-4 py-2 bg-stone-50 rounded-lg text-center">
					<p class="text-lg font-bold text-stone-600">{bs.size_grams}g</p>
				</div>
			{/each}
		</div>
	</div>
</div>
