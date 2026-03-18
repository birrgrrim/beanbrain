<script lang="ts">
	import { api, type Equipment, type BrewMethod, type BasketSize } from '$lib/api';
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';

	let equipmentList = $state<Equipment[]>([]);
	let brewMethods = $state<BrewMethod[]>([]);
	let basketSizes = $state<BasketSize[]>([]);

	let newGrinderName = $state('');
	let newMachineName = $state('');
	let newMethodName = $state('');
	let newBasketGrams = $state('');

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

	async function addEquipment(type: string, name: string) {
		if (!name.trim()) return;
		await api.equipment.create({ type, name: name.trim() });
		if (type === 'grinder') newGrinderName = '';
		else newMachineName = '';
		await load();
	}

	async function setDefault(id: number) {
		await api.equipment.update(id, { is_default: true });
		await load();
	}

	async function deleteEquipment(id: number) {
		await api.equipment.delete(id);
		await load();
	}

	async function addMethod() {
		if (!newMethodName.trim()) return;
		await api.equipment.createBrewMethod({ name: newMethodName.trim() });
		newMethodName = '';
		await load();
	}

	async function deleteMethod(id: number) {
		await api.equipment.deleteBrewMethod(id);
		await load();
	}

	async function addBasket() {
		const grams = parseInt(newBasketGrams);
		if (!grams) return;
		await api.equipment.createBasketSize({ size_grams: grams, label: `${grams}g` });
		newBasketGrams = '';
		await load();
	}

	async function deleteBasket(id: number) {
		await api.equipment.deleteBasketSize(id);
		await load();
	}
</script>

<div class="max-w-lg mx-auto p-6 space-y-6">
	<div class="flex items-center gap-4">
		<img src="/img/empty-grinder.png" alt="" class="opacity-70" style="width: 48px;" />
		<h2 class="text-2xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
			{$t('grinders.title')}
		</h2>
	</div>

	<!-- Grinders -->
	<div class="bg-card rounded-2xl border border-stone-100 shadow-sm p-5">
		<div class="flex items-center gap-2 mb-3">
			<Icons icon="grinder" size={18} className="text-stone-400" />
			<h3 class="font-semibold text-stone-700">{$t('grinders.grinders')}</h3>
		</div>
		{#each grinders as g}
			<div class="flex items-center justify-between py-2 px-2 rounded-lg hover:bg-card-inset">
				<div class="flex items-center gap-2">
					<span class="text-base text-stone-700">{g.name}</span>
					{#if g.model}<span class="text-xs text-stone-300">{g.model}</span>{/if}
					{#if g.is_default}<span class="px-1.5 py-0.5 text-xs bg-amber-100 text-amber-700 rounded-md px-2 py-0.5">default</span>{/if}
				</div>
				<div class="flex gap-1">
					{#if !g.is_default}
						<button onclick={() => setDefault(g.id)} class="px-1.5 py-0.5 text-sm text-stone-400 hover:text-amber-600 rounded hover:bg-card-inset px-2 py-1">set default</button>
					{/if}
					<button onclick={() => deleteEquipment(g.id)} class="p-1.5 text-stone-300 hover:text-red-400 rounded hover:bg-card-inset" title={$t('detail.delete')}>
						<Icons icon="delete" size={18} />
					</button>
				</div>
			</div>
		{/each}
		<div class="flex gap-2 mt-2">
			<input type="text" bind:value={newGrinderName} placeholder="Add grinder..."
				class="flex-1 px-4 py-2 rounded-lg border border-stone-200 text-base focus:outline-none focus:ring-2 focus:ring-amber-400/50"
				onkeydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addEquipment('grinder', newGrinderName); } }} />
			<button onclick={() => addEquipment('grinder', newGrinderName)} disabled={!newGrinderName.trim()}
				class="px-4 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800 disabled:opacity-50">{$t('persons.add')}</button>
		</div>
	</div>

	<!-- Machines -->
	<div class="bg-card rounded-2xl border border-stone-100 shadow-sm p-5">
		<div class="flex items-center gap-2 mb-3">
			<Icons icon="cup" size={18} className="text-stone-400" />
			<h3 class="font-semibold text-stone-700">{$t('grinders.machines')}</h3>
		</div>
		{#each machines as m}
			<div class="flex items-center justify-between py-2 px-2 rounded-lg hover:bg-card-inset">
				<div class="flex items-center gap-2">
					<span class="text-base text-stone-700">{m.name}</span>
					{#if m.is_default}<span class="px-1.5 py-0.5 text-xs bg-amber-100 text-amber-700 rounded-md px-2 py-0.5">default</span>{/if}
				</div>
				<div class="flex gap-1">
					{#if !m.is_default}
						<button onclick={() => setDefault(m.id)} class="px-1.5 py-0.5 text-sm text-stone-400 hover:text-amber-600 rounded hover:bg-card-inset px-2 py-1">set default</button>
					{/if}
					<button onclick={() => deleteEquipment(m.id)} class="p-1.5 text-stone-300 hover:text-red-400 rounded hover:bg-card-inset" title={$t('detail.delete')}>
						<Icons icon="delete" size={18} />
					</button>
				</div>
			</div>
		{/each}
		<div class="flex gap-2 mt-2">
			<input type="text" bind:value={newMachineName} placeholder="Add machine..."
				class="flex-1 px-4 py-2 rounded-lg border border-stone-200 text-base focus:outline-none focus:ring-2 focus:ring-amber-400/50"
				onkeydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addEquipment('machine', newMachineName); } }} />
			<button onclick={() => addEquipment('machine', newMachineName)} disabled={!newMachineName.trim()}
				class="px-4 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800 disabled:opacity-50">{$t('persons.add')}</button>
		</div>
	</div>

	<!-- Brew Methods -->
	<div class="bg-card rounded-2xl border border-stone-100 shadow-sm p-5">
		<div class="flex items-center gap-2 mb-3">
			<Icons icon="bean" size={18} className="text-stone-400" />
			<h3 class="font-semibold text-stone-700">{$t('grinders.brew_methods')}</h3>
		</div>
		{#each brewMethods as m}
			<div class="flex items-center justify-between py-2 px-2 rounded-lg hover:bg-card-inset">
				<div class="flex items-center gap-2">
					<span class="text-base text-stone-700">{m.name}</span>
					{#if m.is_default}<span class="px-1.5 py-0.5 text-xs bg-amber-100 text-amber-700 rounded-md px-2 py-0.5">default</span>{/if}
				</div>
				<button onclick={() => deleteMethod(m.id)} class="p-1.5 text-stone-300 hover:text-red-400 rounded hover:bg-card-inset" title={$t('detail.delete')}>
					<Icons icon="delete" size={18} />
				</button>
			</div>
		{/each}
		<div class="flex gap-2 mt-2">
			<input type="text" bind:value={newMethodName} placeholder="Add method..."
				class="flex-1 px-4 py-2 rounded-lg border border-stone-200 text-base focus:outline-none focus:ring-2 focus:ring-amber-400/50"
				onkeydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addMethod(); } }} />
			<button onclick={addMethod} disabled={!newMethodName.trim()}
				class="px-4 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800 disabled:opacity-50">{$t('persons.add')}</button>
		</div>
	</div>

	<!-- Basket Sizes -->
	<div class="bg-card rounded-2xl border border-stone-100 shadow-sm p-5">
		<div class="flex items-center gap-2 mb-3">
			<Icons icon="settings" size={18} className="text-stone-400" />
			<h3 class="font-semibold text-stone-700">{$t('grinders.baskets')}</h3>
		</div>
		<div class="flex flex-wrap gap-2 mb-3">
			{#each basketSizes as bs}
				<div class="flex items-center gap-1 px-3 py-2 bg-card-inset rounded-lg {bs.is_default ? 'ring-2 ring-amber-300' : ''}">
					<span class="text-sm font-bold text-stone-600">{bs.size_grams}g</span>
					<button onclick={() => deleteBasket(bs.id)} class="ml-1 text-stone-300 hover:text-red-400" title={$t('detail.delete')}>
						<Icons icon="delete" size={18} />
					</button>
				</div>
			{/each}
		</div>
		<div class="flex gap-2">
			<input type="number" bind:value={newBasketGrams} placeholder="grams"
				class="w-24 px-4 py-2 rounded-lg border border-stone-200 text-base focus:outline-none focus:ring-2 focus:ring-amber-400/50"
				onkeydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addBasket(); } }} />
			<button onclick={addBasket} disabled={!newBasketGrams}
				class="px-4 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800 disabled:opacity-50">{$t('persons.add')}</button>
		</div>
	</div>
</div>
