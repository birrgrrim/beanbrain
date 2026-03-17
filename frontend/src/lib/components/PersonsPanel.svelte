<script lang="ts">
	import { api, type Taster } from '$lib/api';
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';

	let tasters = $state<Taster[]>([]);
	let newName = $state('');

	async function load() {
		tasters = await api.tasters.list();
	}

	$effect(() => { load(); });

	async function add() {
		if (!newName.trim()) return;
		await api.tasters.create(newName.trim());
		newName = '';
		await load();
	}

	async function remove(id: number) {
		await api.tasters.delete(id);
		await load();
	}
</script>

<div class="max-w-lg mx-auto p-6 space-y-6">
	<h2 class="text-2xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
		{$t('persons.title')}
	</h2>

	<div class="bg-white rounded-2xl border border-stone-100 shadow-sm p-5">
		<p class="text-xs text-stone-300 uppercase tracking-wide mb-4">{$t('persons.subtitle')}</p>

		{#if tasters.length === 0}
			<div class="text-center py-6">
				<Icons icon="cup" size={32} className="mx-auto text-stone-200 mb-2" />
				<p class="text-sm text-stone-300">{$t('persons.empty')}</p>
			</div>
		{:else}
			<div class="space-y-1 mb-4">
				{#each tasters as taster}
					<div class="flex items-center justify-between py-2.5 px-3 rounded-lg hover:bg-stone-50 transition-colors">
						<span class="text-sm font-medium text-stone-700">{taster.name}</span>
						<button onclick={() => remove(taster.id)}
							class="p-1 text-stone-200 hover:text-red-400 transition-colors" title="Remove">
							<Icons icon="delete" size={14} />
						</button>
					</div>
				{/each}
			</div>
		{/if}

		<div class="flex gap-2">
			<input type="text" bind:value={newName} placeholder={$t('persons.add_placeholder')}
				class="flex-1 px-3 py-2 rounded-lg border border-stone-200 text-sm bg-white
					focus:outline-none focus:ring-2 focus:ring-amber-400/50"
				onkeydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); add(); } }}
			/>
			<button onclick={add} disabled={!newName.trim()}
				class="px-4 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800
					transition-colors disabled:opacity-50 disabled:cursor-not-allowed">{$t('persons.add')}</button>
		</div>
	</div>
</div>
