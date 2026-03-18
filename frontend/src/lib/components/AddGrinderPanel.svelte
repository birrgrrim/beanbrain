<script lang="ts">
	import { api } from '$lib/api';
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';

	let { onCreated, onCancel }: {
		onCreated: (id: number) => void;
		onCancel: () => void;
	} = $props();

	let name = $state('');
	let model = $state('');
	let kind = $state<'auto' | 'manual'>('auto');
	let saving = $state(false);

	async function save() {
		if (!name.trim()) return;
		saving = true;
		const grinder = await api.grinders.create({
			name: name.trim(),
			model: model.trim() || undefined,
			kind,
		});
		saving = false;
		onCreated(grinder.id);
	}
</script>

<div class="max-w-2xl mx-auto p-10 space-y-6">
	<div class="flex items-center gap-3">
		<button onclick={onCancel}
			class="p-1.5 text-stone-400 hover:text-stone-600 transition-colors rounded-lg hover:bg-card-inset"
			title="Back">
			<Icons icon="back" size={18} />
		</button>
		<img src="/img/grinder-{kind}.png" alt="" class="w-8 h-8 opacity-70" />
		<h2 class="text-3xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
			{$t('grinding.add')}
		</h2>
	</div>

	<div class="bg-card rounded-2xl border border-stone-100 shadow-sm p-6 space-y-4">
		<div class="flex gap-3">
			<button onclick={() => kind = 'auto'}
				class="flex-1 flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-colors
					{kind === 'auto' ? 'border-amber-400 bg-amber-50/50' : 'border-stone-100 hover:border-stone-200'}">
				<img src="/img/grinder-auto.png" alt="" class="w-12 h-12 opacity-70" />
				<span class="text-sm font-medium {kind === 'auto' ? 'text-amber-700' : 'text-stone-400'}">Auto</span>
			</button>
			<button onclick={() => kind = 'manual'}
				class="flex-1 flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-colors
					{kind === 'manual' ? 'border-amber-400 bg-amber-50/50' : 'border-stone-100 hover:border-stone-200'}">
				<img src="/img/grinder-manual.png" alt="" class="w-12 h-12 opacity-70" />
				<span class="text-sm font-medium {kind === 'manual' ? 'text-amber-700' : 'text-stone-400'}">Manual</span>
			</button>
		</div>
		<div>
			<label for="grinder-name" class="text-xs text-stone-400 uppercase tracking-wide">{$t('grinding.name')}</label>
			<input id="grinder-name" type="text" bind:value={name} placeholder={$t('grinding.name_placeholder')}
				class="w-full mt-1 px-4 py-2.5 rounded-lg border border-stone-200 text-base bg-card-inset
					focus:outline-none focus:ring-2 focus:ring-amber-400/50 focus:border-amber-300" />
		</div>
		<div>
			<label for="grinder-model" class="text-xs text-stone-400 uppercase tracking-wide">{$t('grinding.model')}</label>
			<input id="grinder-model" type="text" bind:value={model} placeholder={$t('grinding.model_placeholder')}
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
