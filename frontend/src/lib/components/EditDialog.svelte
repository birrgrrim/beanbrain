<script lang="ts">
	import { api, type Grinder, type BrewSetup, type Taster, type BrewMethodType } from '$lib/api';
	import { t } from '$lib/i18n';

	type DialogType =
		| { type: 'person'; mode: 'add' }
		| { type: 'person'; mode: 'edit'; item: Taster }
		| { type: 'grinder'; mode: 'add' }
		| { type: 'grinder'; mode: 'edit'; item: Grinder }
		| { type: 'brew'; mode: 'add' }
		| { type: 'brew'; mode: 'edit'; item: BrewSetup };

	let {
		dialog,
		brewMethodTypes = [],
		onSaved,
		onDeleted,
		onClose,
	}: {
		dialog: DialogType;
		brewMethodTypes?: BrewMethodType[];
		onSaved: () => void;
		onDeleted: () => void;
		onClose: () => void;
	} = $props();

	// Person fields
	let personName = $state('');

	// Grinder fields
	let gManufacturer = $state('');
	let gModel = $state('');
	let gKind = $state<'auto' | 'manual'>('auto');
	let gRangeMin = $state<number | string>(0);
	let gRangeMax = $state<number | string>('');
	let gStep = $state<number | string>(1);

	// Brew setup fields
	let bManufacturer = $state('');
	let bModel = $state('');
	let bMethodType = $state('espresso');
	let bBasketGrams = $state<number | string>('');

	let saving = $state(false);
	let confirmDelete = $state(false);
	let deleteInfo = $state('');

	// Initialize fields from dialog prop
	$effect(() => {
		confirmDelete = false;
		deleteInfo = '';
		if (dialog.type === 'person') {
			personName = dialog.mode === 'edit' ? dialog.item.name : '';
		} else if (dialog.type === 'grinder') {
			if (dialog.mode === 'edit') {
				gManufacturer = dialog.item.manufacturer;
				gModel = dialog.item.model ?? '';
				gKind = dialog.item.kind as 'auto' | 'manual';
				gRangeMin = dialog.item.range_min;
				gRangeMax = dialog.item.range_max ?? '';
				gStep = dialog.item.step;
			} else {
				gManufacturer = ''; gModel = ''; gKind = 'auto';
				gRangeMin = 0; gRangeMax = ''; gStep = 1;
			}
		} else if (dialog.type === 'brew') {
			if (dialog.mode === 'edit') {
				bManufacturer = dialog.item.manufacturer;
				bModel = dialog.item.model ?? '';
				bMethodType = dialog.item.method_type;
				bBasketGrams = dialog.item.basket_grams ?? '';
			} else {
				bManufacturer = ''; bModel = ''; bMethodType = 'espresso'; bBasketGrams = '';
			}
		}
	});

	const hasBasket = $derived(
		brewMethodTypes.find(m => m.key === bMethodType)?.has_basket ?? false
	);

	const canSave = $derived(
		dialog.type === 'person' ? personName.trim().length > 0 :
		dialog.type === 'grinder' ? gManufacturer.trim().length > 0 :
		bManufacturer.trim().length > 0
	);

	async function save() {
		if (!canSave) return;
		saving = true;
		try {
			if (dialog.type === 'person') {
				if (dialog.mode === 'edit') {
					await api.tasters.update(dialog.item.id, { name: personName.trim() });
				} else {
					await api.tasters.create(personName.trim());
				}
			} else if (dialog.type === 'grinder') {
				const data = {
					manufacturer: gManufacturer.trim(),
					model: gModel.trim() || undefined,
					kind: gKind,
					range_min: Number(gRangeMin) || 0,
					range_max: gRangeMax !== '' ? Number(gRangeMax) : null,
					step: Number(gStep) || 1,
				};
				if (dialog.mode === 'edit') {
					await api.grinders.update(dialog.item.id, data);
				} else {
					await api.grinders.create(data);
				}
			} else if (dialog.type === 'brew') {
				const data: Record<string, unknown> = {
					manufacturer: bManufacturer.trim(),
					model: bModel.trim() || undefined,
					method_type: bMethodType,
					basket_grams: hasBasket && bBasketGrams ? Number(bBasketGrams) : null,
				};
				if (dialog.mode === 'edit') {
					await api.brewSetups.update(dialog.item.id, data);
				} else {
					await api.brewSetups.create(data as Parameters<typeof api.brewSetups.create>[0]);
				}
			}
			onSaved();
		} finally {
			saving = false;
		}
	}

	async function startDelete() {
		if (dialog.mode !== 'edit') return;
		// Fetch dependents
		let info = '';
		if (dialog.type === 'person') {
			const deps = await api.tasters.dependents(dialog.item.id);
			if (deps.reviews > 0) info = `${deps.reviews} review(s) will be deleted`;
		} else if (dialog.type === 'grinder') {
			const deps = await api.grinders.dependents(dialog.item.id);
			if (deps.grinder_settings > 0) info = `${deps.grinder_settings} grinder setting(s) will be deleted`;
		} else if (dialog.type === 'brew') {
			const deps = await api.brewSetups.dependents(dialog.item.id);
			const parts = [];
			if (deps.grinder_settings > 0) parts.push(`${deps.grinder_settings} grinder setting(s)`);
			if (deps.reviews > 0) parts.push(`${deps.reviews} review(s)`);
			info = parts.length > 0 ? `${parts.join(' and ')} will be deleted` : '';
		}
		deleteInfo = info;
		confirmDelete = true;
	}

	async function doDelete() {
		if (dialog.mode !== 'edit') return;
		if (dialog.type === 'person') await api.tasters.delete(dialog.item.id);
		else if (dialog.type === 'grinder') await api.grinders.delete(dialog.item.id);
		else if (dialog.type === 'brew') await api.brewSetups.delete(dialog.item.id);
		onDeleted();
	}
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="fixed inset-0 bg-black/30 z-50 flex items-center justify-center" onclick={onClose}>
	<div class="bg-card rounded-2xl border border-stone-200 shadow-xl w-full max-w-lg mx-4 p-6 space-y-4"
		onclick={(e) => e.stopPropagation()}>

		<h3 class="text-xl font-bold text-stone-800" style="font-family: 'DM Serif Display', serif;">
			{#if dialog.type === 'person'}
				{dialog.mode === 'edit' ? $t('person.edit') : $t('person.add_new')}
			{:else if dialog.type === 'grinder'}
				{dialog.mode === 'edit' ? $t('grinding.edit') : $t('grinding.add')}
			{:else}
				{dialog.mode === 'edit' ? $t('brewing.edit') : $t('brewing.add')}
			{/if}
		</h3>

		{#if confirmDelete}
			<div class="space-y-3">
				<p class="text-sm text-stone-600">{$t('common.delete_confirm')}</p>
				{#if deleteInfo}
					<p class="text-sm text-red-500">{deleteInfo}</p>
				{/if}
				<div class="flex gap-2 justify-end">
					<button onclick={() => confirmDelete = false} class="px-4 py-2 text-stone-400 text-sm">{$t('common.cancel')}</button>
					<button onclick={doDelete} class="px-4 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700">{$t('detail.delete')}</button>
				</div>
			</div>
		{:else}
			<!-- Person form -->
			{#if dialog.type === 'person'}
				<div>
					<label for="person-name" class="text-xs text-stone-400 uppercase tracking-wide">{$t('persons.name')}</label>
					<input id="person-name" type="text" bind:value={personName} placeholder={$t('persons.add_placeholder')}
						class="w-full mt-1 px-4 py-2.5 rounded-lg border border-stone-200 text-base bg-card-inset
							focus:outline-none focus:ring-2 focus:ring-amber-400/50"
						onkeydown={(e) => { if (e.key === 'Enter') save(); }} />
				</div>

			<!-- Grinder form -->
			{:else if dialog.type === 'grinder'}
				{#if dialog.mode === 'add'}
					<div class="flex gap-3">
						<button onclick={() => gKind = 'auto'}
							class="flex-1 flex flex-col items-center gap-1 p-3 rounded-xl border-2 transition-colors
								{gKind === 'auto' ? 'border-amber-400 bg-amber-50/50' : 'border-stone-100 hover:border-stone-200'}">
							<img src="/img/grinder-auto.png" alt="" class="w-10 h-10 opacity-70" />
							<span class="text-xs font-medium {gKind === 'auto' ? 'text-amber-700' : 'text-stone-400'}">Auto</span>
						</button>
						<button onclick={() => gKind = 'manual'}
							class="flex-1 flex flex-col items-center gap-1 p-3 rounded-xl border-2 transition-colors
								{gKind === 'manual' ? 'border-amber-400 bg-amber-50/50' : 'border-stone-100 hover:border-stone-200'}">
							<img src="/img/grinder-manual.png" alt="" class="w-10 h-10 opacity-70" />
							<span class="text-xs font-medium {gKind === 'manual' ? 'text-amber-700' : 'text-stone-400'}">Manual</span>
						</button>
					</div>
				{:else}
					<div class="flex items-center gap-2">
						<img src="/img/grinder-{gKind}.png" alt="" class="w-8 h-8 opacity-60" />
						<span class="text-sm text-stone-500">{gKind === 'manual' ? 'Manual' : 'Auto'}</span>
					</div>
				{/if}
				<div>
					<label for="g-manufacturer" class="text-xs text-stone-400 uppercase tracking-wide">{$t('grinding.manufacturer')}</label>
					<input id="g-manufacturer" type="text" bind:value={gManufacturer} placeholder={$t('grinding.manufacturer_placeholder')}
						class="w-full mt-1 px-4 py-2.5 rounded-lg border border-stone-200 text-base bg-card-inset
							focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
				</div>
				<div>
					<label for="g-model" class="text-xs text-stone-400 uppercase tracking-wide">{$t('grinding.model')}</label>
					<input id="g-model" type="text" bind:value={gModel} placeholder={$t('grinding.model_placeholder')}
						class="w-full mt-1 px-4 py-2.5 rounded-lg border border-stone-200 text-base bg-card-inset
							focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
				</div>
				<div>
					<label class="text-xs text-stone-400 uppercase tracking-wide">{$t('grinding.range')}</label>
					<div class="flex items-center gap-2 mt-1">
						<input type="number" bind:value={gRangeMin} placeholder="0"
							class="w-20 px-3 py-2 rounded-lg border border-stone-200 text-base bg-card-inset text-center
								focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
						<span class="text-stone-400">—</span>
						<input type="number" bind:value={gRangeMax} placeholder="∞"
							class="w-20 px-3 py-2 rounded-lg border border-stone-200 text-base bg-card-inset text-center
								focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
						<span class="text-xs text-stone-400 mx-1">{$t('grinding.step')}</span>
						<input type="number" bind:value={gStep} placeholder="1" min="0.1" step="0.1"
							class="w-16 px-3 py-2 rounded-lg border border-stone-200 text-base bg-card-inset text-center
								focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
					</div>
				</div>

			<!-- Brew setup form -->
			{:else if dialog.type === 'brew'}
				{#if dialog.mode === 'add'}
					<div>
						<label class="text-xs text-stone-400 uppercase tracking-wide">{$t('brewing.method')}</label>
						<div class="grid grid-cols-3 gap-2 mt-1">
							{#each brewMethodTypes as method}
								<button onclick={() => bMethodType = method.key}
									class="flex flex-col items-center gap-1 p-2 rounded-xl border-2 transition-colors
										{bMethodType === method.key ? 'border-amber-400 bg-amber-50/50' : 'border-stone-100 hover:border-stone-200'}">
									<img src="/img/{method.icon}" alt="" class="w-8 h-8 opacity-70" />
									<span class="text-[10px] font-medium truncate w-full text-center
										{bMethodType === method.key ? 'text-amber-700' : 'text-stone-400'}">{$t(`method.${method.key}`)}</span>
								</button>
							{/each}
						</div>
					</div>
				{:else}
					{@const methodIcon = brewMethodTypes.find(m => m.key === bMethodType)?.icon ?? 'method-espresso.png'}
					<div class="flex items-center gap-2">
						<img src="/img/{methodIcon}" alt="" class="w-8 h-8 opacity-60" />
						<span class="text-sm text-stone-500">{$t(`method.${bMethodType}`)}</span>
					</div>
				{/if}
				<div>
					<label for="b-manufacturer" class="text-xs text-stone-400 uppercase tracking-wide">{$t('brewing.manufacturer')}</label>
					<input id="b-manufacturer" type="text" bind:value={bManufacturer} placeholder={$t('brewing.manufacturer_placeholder')}
						class="w-full mt-1 px-4 py-2.5 rounded-lg border border-stone-200 text-base bg-card-inset
							focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
				</div>
				<div>
					<label for="b-model" class="text-xs text-stone-400 uppercase tracking-wide">{$t('brewing.model')}</label>
					<input id="b-model" type="text" bind:value={bModel} placeholder={$t('brewing.model_placeholder')}
						class="w-full mt-1 px-4 py-2.5 rounded-lg border border-stone-200 text-base bg-card-inset
							focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
				</div>
				{#if hasBasket}
					<div>
						<label for="b-basket" class="text-xs text-stone-400 uppercase tracking-wide">{$t('brewing.basket')}</label>
						<input id="b-basket" type="number" bind:value={bBasketGrams} placeholder="18"
							class="w-32 mt-1 px-4 py-2.5 rounded-lg border border-stone-200 text-base bg-card-inset
								focus:outline-none focus:ring-2 focus:ring-amber-400/50" />
					</div>
				{/if}
			{/if}

			<!-- Actions -->
			<div class="flex items-center justify-between pt-2">
				{#if dialog.mode === 'edit'}
					<button onclick={startDelete} class="px-3 py-2 text-red-400 hover:text-red-600 text-sm transition-colors">
						{$t('detail.delete')}
					</button>
				{:else}
					<div></div>
				{/if}
				<div class="flex gap-2">
					<button onclick={onClose} class="px-4 py-2 text-stone-400 text-sm">{$t('common.cancel')}</button>
					<button onclick={save} disabled={!canSave || saving}
						class="px-5 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800 disabled:opacity-50">
						{$t('common.save')}
					</button>
				</div>
			</div>
		{/if}
	</div>
</div>
