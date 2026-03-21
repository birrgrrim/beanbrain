<script lang="ts">
	import type { Descriptor, BrewSetup } from '$lib/api';
	import { t } from '$lib/i18n';
	import StarRating from './StarRating.svelte';
	import DescriptorAutocomplete from './DescriptorAutocomplete.svelte';
	import { toggleId } from '$lib/utils';

	let {
		tasterName,
		brewSetups,
		brewSetupId = $bindable(),
		rating = $bindable(),
		comment = $bindable(),
		descriptorIds = $bindable(),
		descriptors,
		suggestedDescriptorIds = [],
		onSave,
		onCancel,
		onDelete,
	}: {
		tasterName: string;
		brewSetups: BrewSetup[];
		brewSetupId: number | null;
		rating: number;
		comment: string;
		descriptorIds: number[];
		descriptors: Descriptor[];
		suggestedDescriptorIds?: number[];
		onSave: () => void;
		onCancel: () => void;
		onDelete?: () => void;
	} = $props();

	function toggleDescriptor(id: number) {
		descriptorIds = toggleId(descriptorIds, id);
	}
</script>

<div class="py-2 space-y-2">
	<div class="flex items-center gap-3">
		<p class="text-lg font-semibold text-stone-700">{tasterName}</p>
		<StarRating {rating} interactive onRate={(v) => rating = v} />
		{#if rating > 0}<span class="text-xs text-stone-400 tabular-nums">{rating}/10</span>{/if}
	</div>
	<textarea bind:value={comment} rows={2} placeholder={$t('tasting.comment_placeholder')}
		class="w-full px-2 py-1.5 rounded border border-stone-200 text-sm bg-card focus:outline-none focus:ring-2 focus:ring-amber-400/50 resize-none"></textarea>
	<DescriptorAutocomplete {descriptors} selected={descriptorIds} suggested={suggestedDescriptorIds} onToggle={toggleDescriptor} />
	<div class="flex items-center justify-between">
		{#if onDelete}
			<button onclick={onDelete} class="text-sm text-red-400 hover:text-red-600 transition-colors">{$t('detail.delete')}</button>
		{:else}
			<div></div>
		{/if}
		<div class="flex gap-2">
			<button onclick={onCancel} class="px-4 py-2 text-stone-400 text-sm">{$t('tasting.cancel')}</button>
			<button onclick={onSave} disabled={rating === 0}
				class="px-4 py-2 bg-amber-700 text-white rounded-lg text-sm hover:bg-amber-800 disabled:opacity-50">{$t('tasting.save')}</button>
		</div>
	</div>
</div>
