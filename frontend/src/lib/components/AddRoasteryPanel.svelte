<script lang="ts">
	import { api } from '$lib/api';
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';

	let { onCreated, onCancel }: {
		onCreated: (id: number) => void;
		onCancel: () => void;
	} = $props();

	let name = $state('');
	let website = $state('');
	let saving = $state(false);

	async function save() {
		if (!name.trim()) return;
		saving = true;
		const roastery = await api.roasteries.create({
			name: name.trim(),
			website: website.trim() || undefined,
		});
		saving = false;
		onCreated(roastery.id);
	}
</script>

<div class="max-w-2xl mx-auto p-10 space-y-6">
	<div class="flex items-center gap-3">
		<button onclick={onCancel}
			class="p-1.5 text-stone-400 hover:text-stone-600 transition-colors rounded-lg hover:bg-card-inset"
			title="Back">
			<Icons icon="back" size={18} />
		</button>
		<img src="/img/roastery.png" alt="" class="w-8 h-8 opacity-70" />
		<h2 class="text-3xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
			{$t('roastery.add')}
		</h2>
	</div>

	<div class="bg-card rounded-2xl border border-stone-100 shadow-sm p-6 space-y-4">
		<div>
			<label for="roastery-name" class="text-xs text-stone-400 uppercase tracking-wide">{$t('roastery.name')}</label>
			<input id="roastery-name" type="text" bind:value={name} placeholder="MadHeads Coffee"
				class="w-full mt-1 px-4 py-2.5 rounded-lg border border-stone-200 text-base bg-card-inset
					focus:outline-none focus:ring-2 focus:ring-amber-400/50 focus:border-amber-300" />
		</div>
		<div>
			<label for="roastery-website" class="text-xs text-stone-400 uppercase tracking-wide">{$t('roastery.website')}</label>
			<input id="roastery-website" type="url" bind:value={website} placeholder="https://madheadscoffee.com"
				class="w-full mt-1 px-4 py-2.5 rounded-lg border border-stone-200 text-base bg-card-inset
					focus:outline-none focus:ring-2 focus:ring-amber-400/50 focus:border-amber-300" />
		</div>
		<div class="flex gap-2 pt-2">
			<button onclick={save} disabled={!name.trim() || saving}
				class="px-6 py-2.5 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800 disabled:opacity-50">
				{$t('common.save')}
			</button>
			<button onclick={onCancel} class="px-6 py-2.5 text-stone-400 text-sm">{$t('common.cancel')}</button>
		</div>
	</div>
</div>
