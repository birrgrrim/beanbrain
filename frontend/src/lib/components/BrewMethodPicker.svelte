<script lang="ts">
	import { BREW_METHOD_TYPES } from '$lib/api';
	import { t } from '$lib/i18n';
	import Icons from './Icons.svelte';

	let { onPicked, onCancel }: {
		onPicked: (methodType: string, hasBasket: boolean) => void;
		onCancel: () => void;
	} = $props();

	const methodTypes = BREW_METHOD_TYPES;
</script>

<div class="max-w-2xl mx-auto p-10 space-y-6">
	<div class="flex items-center gap-3">
		<button onclick={onCancel}
			class="p-1.5 text-stone-400 hover:text-stone-600 transition-colors rounded-lg hover:bg-card-inset"
			title="Back">
			<Icons icon="back" size={18} />
		</button>
		<img src="/img/tab-machine.png" alt="" class="w-8 h-8 opacity-70" />
		<h2 class="text-3xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
			{$t('brewing.pick_method')}
		</h2>
	</div>

	<div class="grid grid-cols-3 gap-4">
		{#each methodTypes as mt}
			<button
				onclick={() => onPicked(mt.key, mt.has_basket)}
				class="bg-card rounded-2xl border border-stone-100 shadow-sm p-6 flex flex-col items-center gap-3
					hover:border-amber-300 hover:shadow-md transition-[color,background-color,border-color,box-shadow] duration-150 cursor-pointer"
			>
				<img src="/img/{mt.icon}" alt="" class="w-16 h-16 opacity-70" />
				<span class="font-semibold text-stone-700">{$t(`method.${mt.key}`)}</span>
			</button>
		{/each}
	</div>
</div>
