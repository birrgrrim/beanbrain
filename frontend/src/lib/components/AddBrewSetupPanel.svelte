<script lang="ts">
	import { api } from '$lib/api';
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';

	let { methodType, hasBasket, onCreated, onCancel }: {
		methodType: string;
		hasBasket: boolean;
		onCreated: (id: number) => void;
		onCancel: () => void;
	} = $props();

	let name = $state('');
	let basketGrams = $state('');
	let saving = $state(false);

	async function save() {
		if (!name.trim()) return;
		saving = true;
		const setup = await api.brewSetups.create({
			method_type: methodType,
			name: name.trim(),
			basket_grams: hasBasket && basketGrams ? parseInt(basketGrams) : undefined,
		});
		saving = false;
		onCreated(setup.id);
	}
</script>

<div class="max-w-2xl mx-auto p-10 space-y-6">
	<div class="flex items-center gap-3">
		<button onclick={onCancel}
			class="p-1.5 text-stone-400 hover:text-stone-600 transition-colors rounded-lg hover:bg-card-inset"
			title="Back">
			<Icons icon="back" size={18} />
		</button>
		<img src="/img/method-{methodType}.png" alt="" class="w-8 h-8 opacity-70" />
		<h2 class="text-3xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
			{$t(`method.${methodType}`)}
		</h2>
	</div>

	<div class="bg-card rounded-2xl border border-stone-100 shadow-sm p-6 space-y-4">
		<div>
			<label for="brew-setup-name" class="text-xs text-stone-400 uppercase tracking-wide">{$t('brewing.name')}</label>
			<input id="brew-setup-name" type="text" bind:value={name} placeholder={$t('brewing.name_placeholder')}
				class="w-full mt-1 px-4 py-2.5 rounded-lg border border-stone-200 text-base bg-card-inset
					focus:outline-none focus:ring-2 focus:ring-amber-400/50 focus:border-amber-300" />
		</div>
		{#if hasBasket}
			<div>
				<label for="brew-setup-basket" class="text-xs text-stone-400 uppercase tracking-wide">{$t('brewing.basket')}</label>
				<input id="brew-setup-basket" type="number" bind:value={basketGrams} placeholder="18"
					class="w-32 mt-1 px-4 py-2.5 rounded-lg border border-stone-200 text-base bg-card-inset
						focus:outline-none focus:ring-2 focus:ring-amber-400/50 focus:border-amber-300" />
			</div>
		{/if}
		<div class="flex gap-2 pt-2">
			<button onclick={save} disabled={!name.trim() || saving}
				class="px-6 py-2.5 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800 disabled:opacity-50">
				{$t('common.save')}
			</button>
			<button onclick={onCancel} class="px-6 py-2.5 text-stone-400 text-sm">{$t('common.cancel')}</button>
		</div>
	</div>
</div>
