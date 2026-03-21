<script lang="ts">
	import { api, type BrewSetup } from '$lib/api';
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';

	let { brewSetup, onUpdated, onDeleted, onBack }: {
		brewSetup: BrewSetup;
		onUpdated: () => void;
		onDeleted: () => void;
		onBack: () => void;
	} = $props();

	async function toggleDefault() {
		await api.brewSetups.update(brewSetup.id, { is_default: !brewSetup.is_default });
		onUpdated();
	}

	async function deleteSetup() {
		if (!confirm(`Delete "${brewSetup.manufacturer}"?`)) return;
		await api.brewSetups.delete(brewSetup.id);
		onDeleted();
	}
</script>

<div class="max-w-2xl mx-auto p-10 space-y-8">
	<div class="flex items-start justify-between">
		<div class="flex items-center gap-3">
			<button onclick={onBack}
				class="p-1.5 text-stone-400 hover:text-stone-600 transition-colors rounded-lg hover:bg-card-inset"
				title="Back">
				<Icons icon="back" size={18} />
			</button>
			<img src="/img/method-{brewSetup.method_type}.png" alt="" class="w-8 h-8 opacity-70" />
			<h2 class="text-3xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
				{brewSetup.manufacturer}
			</h2>
		</div>
		<button onclick={deleteSetup}
			class="p-2 text-stone-400 hover:text-red-500 transition-colors rounded hover:bg-card-inset"
			title={$t('detail.delete')}>
			<img src="/img/knockbox.png" alt="delete" class="w-7 h-7 opacity-50" />
		</button>
	</div>

	<div class="bg-card rounded-2xl border border-stone-100 shadow-sm animate-card p-6 space-y-4">
		<div class="flex items-center gap-4">
			<img src="/img/method-{brewSetup.method_type}.png" alt="" class="w-16 h-16 opacity-60" />
			<div class="space-y-1">
				<p class="text-stone-700 font-medium text-lg">{brewSetup.manufacturer}</p>
				{#if brewSetup.model}<p class="text-sm text-stone-400">{brewSetup.model}</p>{/if}
				<p class="text-sm text-stone-400">{$t(`method.${brewSetup.method_type}`)}</p>
				{#if brewSetup.basket_grams}
					<div class="flex items-center gap-2">
						<img src="/img/basket-size.png" alt="" class="w-4 h-4 opacity-50" />
						<span class="text-sm text-stone-500">{brewSetup.basket_grams}g basket</span>
					</div>
				{/if}
			</div>
		</div>

		<div class="flex items-center gap-4 pt-2">
			<button onclick={toggleDefault}
				class="relative inline-flex h-6 w-12 items-center rounded-full transition-colors
					{brewSetup.is_default ? 'bg-amber-600' : 'bg-stone-300'}"
				title={$t('common.set_default')}
			>
				<span class="inline-block h-4 w-4 rounded-full bg-white shadow transition-transform
					{brewSetup.is_default ? 'translate-x-7' : 'translate-x-1'}"></span>
			</button>
			<span class="text-sm text-stone-500">{$t('common.default')}</span>
		</div>
	</div>
</div>
