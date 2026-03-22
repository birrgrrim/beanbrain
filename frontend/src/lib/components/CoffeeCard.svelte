<script lang="ts">
	import type { CoffeeListItem } from '$lib/api';
	import type { AppMode } from '$lib/modeStore';
	import { t } from '$lib/i18n';
	import { lang } from '$lib/lang';
	import GrindValue from './GrindValue.svelte';

	let { coffee, mode, onClick }: {
		coffee: CoffeeListItem;
		mode: AppMode;
		onClick: (id: number) => void;
	} = $props();

	let currentLang = $state('en');
	lang.subscribe(v => currentLang = v);

	const originName = $derived(
		coffee.origin_ref
			? (currentLang === 'uk' ? coffee.origin_ref.name_uk : coffee.origin_ref.name_en)
			: null
	);

	const displayPrice = $derived(coffee.price ? `${coffee.price}₴` : null);
	const ratingDisplay = $derived(coffee.person_rating != null ? coffee.person_rating : null);
	const avgRatingDisplay = $derived(coffee.avg_rating != null ? Math.round(coffee.avg_rating) : null);
	const dimmed = $derived(!coffee.in_stock && !coffee.in_store);
	const descriptorNames = $derived(coffee.roastery_descriptors.slice(0, 5).map(d => d.name));
	const hasTaste = $derived(coffee.sweetness != null || coffee.acidity != null || coffee.bitterness != null);
</script>

<button
	onclick={() => onClick(coffee.id)}
	class="card text-left w-full {dimmed ? 'opacity-40' : ''}"
>
	<!-- COMPACT LAYOUT (mobile/iPad <1024px): name on top, image+info below -->
	<div class="compact-only">
		<div class="c-top">
			<h3 class="c-title">
				{#if coffee.origin_ref?.flag}<span class="flag">{coffee.origin_ref.flag}</span>{/if}
				{coffee.name}
				{#if originName}<span class="c-country">{originName}</span>{/if}
			</h3>
			{#if mode === 'my-coffee' && coffee.in_stock}<span class="badge badge-open badge-sm">{$t('card.open')}</span>{/if}
			{#if mode === 'discover' && coffee.in_store}<span class="badge badge-store badge-sm">{$t('card.inStore')}</span>{/if}
		</div>
		<div class="c-bottom">
			<div class="c-image">
				{#if coffee.image_url}<img src={coffee.image_url} alt="" class="w-full h-full object-contain" />
				{:else}<img src="/img/coffee-placeholder.png" alt="" class="w-12 h-12 opacity-30" />{/if}
			</div>
			<div class="c-info">
				<div class="c-mid">
					{#if hasTaste}
						<div class="taste-col">
							{#if coffee.sweetness != null}<div class="taste-item"><span class="taste-lbl ts">{$t('card.sweet')}</span><div class="taste-bg ts"><div class="taste-fill" style="width:{coffee.sweetness*10}%"></div></div><span class="taste-num ts">{coffee.sweetness}</span></div>{/if}
							{#if coffee.acidity != null}<div class="taste-item"><span class="taste-lbl ts">{$t('card.acid')}</span><div class="taste-bg ts"><div class="taste-fill" style="width:{coffee.acidity*10}%"></div></div><span class="taste-num ts">{coffee.acidity}</span></div>{/if}
							{#if coffee.bitterness != null}<div class="taste-item"><span class="taste-lbl ts">{$t('card.bitter')}</span><div class="taste-bg ts"><div class="taste-fill" style="width:{coffee.bitterness*10}%"></div></div><span class="taste-num ts">{coffee.bitterness}</span></div>{/if}
						</div>
					{/if}
					<div class="met-col">
						{#if mode === 'my-coffee'}
							{#if coffee.default_grind != null}<div class="met ms"><img src="/img/icon-grind.png" alt="" class="met-ico mis" /><GrindValue value={coffee.default_grind} step={coffee.default_grind_step} class="met-val mvs" /></div>{/if}
							{#if ratingDisplay}<div class="met ms"><img src="/img/icon-rating.png" alt="" class="met-ico mis" /><span class="met-val mvs">{ratingDisplay}</span></div>{/if}
						{:else}
							{#if avgRatingDisplay}<div class="met ms"><img src="/img/icon-rating.png" alt="" class="met-ico mis" /><span class="met-val mvs">{avgRatingDisplay}</span></div>{/if}
							{#if displayPrice}<div class="met ms"><span class="met-price mps">{displayPrice}</span></div>{/if}
						{/if}
					</div>
				</div>
				{#if descriptorNames.length > 0}
					<div class="desc-row ds">{#each descriptorNames as n}<span class="desc ds">{n}</span>{/each}</div>
				{/if}
			</div>
		</div>
	</div>

	<!-- HORIZONTAL LAYOUT (1024px+): image left, info right — scales via CSS -->
	<div class="horiz-only">
		<div class="h-image">
			{#if coffee.image_url}<img src={coffee.image_url} alt="" class="w-full h-full object-contain" />
			{:else}<img src="/img/coffee-placeholder.png" alt="" class="w-16 h-16 opacity-30" />{/if}
		</div>
		<div class="h-body">
			<div class="h-header">
				<h3 class="h-title">
					{#if coffee.origin_ref?.flag}<span class="flag">{coffee.origin_ref.flag}</span>{/if}
					{coffee.name}
					{#if originName}<span class="h-country">{originName}</span>{/if}
				</h3>
				{#if mode === 'my-coffee' && coffee.in_stock}<span class="badge badge-open">{$t('card.open')}</span>{/if}
				{#if mode === 'discover' && coffee.in_store}<span class="badge badge-store">{$t('card.inStore')}</span>{/if}
			</div>
			<p class="h-roastery">{coffee.roastery_ref.name}</p>
			<div class="h-mid">
				{#if hasTaste}
					<div class="taste-col">
						{#if coffee.sweetness != null}<div class="taste-item"><span class="taste-lbl">{$t('card.sweet')}</span><div class="taste-bg"><div class="taste-fill" style="width:{coffee.sweetness*10}%"></div></div><span class="taste-num">{coffee.sweetness}</span></div>{/if}
						{#if coffee.acidity != null}<div class="taste-item"><span class="taste-lbl">{$t('card.acid')}</span><div class="taste-bg"><div class="taste-fill" style="width:{coffee.acidity*10}%"></div></div><span class="taste-num">{coffee.acidity}</span></div>{/if}
						{#if coffee.bitterness != null}<div class="taste-item"><span class="taste-lbl">{$t('card.bitter')}</span><div class="taste-bg"><div class="taste-fill" style="width:{coffee.bitterness*10}%"></div></div><span class="taste-num">{coffee.bitterness}</span></div>{/if}
					</div>
				{/if}
				<div class="met-col">
					{#if mode === 'my-coffee'}
						{#if coffee.default_grind != null}<div class="met"><img src="/img/icon-grind.png" alt="" class="met-ico" /><GrindValue value={coffee.default_grind} step={coffee.default_grind_step} class="met-val" /></div>{/if}
						{#if ratingDisplay}<div class="met"><img src="/img/icon-rating.png" alt="" class="met-ico" /><span class="met-val">{ratingDisplay}</span></div>{/if}
					{:else}
						{#if avgRatingDisplay}<div class="met"><img src="/img/icon-rating.png" alt="" class="met-ico" /><span class="met-val">{avgRatingDisplay}</span></div>{/if}
						{#if displayPrice}<div class="met"><span class="met-price">{displayPrice}</span></div>{/if}
					{/if}
				</div>
			</div>
			{#if descriptorNames.length > 0}
				<div class="desc-row">{#each descriptorNames as n}<span class="desc">{n}</span>{/each}</div>
			{/if}
		</div>
	</div>
</button>

<style>
	.card {
		background: var(--color-card);
		border-radius: 0.75rem;
		overflow: hidden;
		border: 1px solid rgba(0, 0, 0, 0.1);
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
		transition: transform 0.15s ease, box-shadow 0.15s ease;
		cursor: pointer;
	}
	.card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08); }

	/* ===== VISIBILITY ===== */
	.compact-only { display: flex; flex-direction: column; }
	.horiz-only { display: none; }
	@media (min-width: 1024px) {
		.compact-only { display: none; }
		.horiz-only { display: flex; flex-direction: row; }
	}

	/* ===== COMPACT (<1024) ===== */
	.c-top { display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; padding: 0.45rem 0.7rem 0.2rem; }
	.c-title { font-family: 'DM Serif Display', serif; font-size: 0.95rem; line-height: 1.25; color: #2c1810; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; min-width: 0; }
	.c-country { font-family: 'DM Sans', sans-serif; font-size: 0.72rem; color: #8c7b6b; font-weight: 400; margin-left: 0.2rem; }
	.c-bottom { display: flex; flex: 1; }
	.c-image { width: 100px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; padding: 0.3rem; }
	.c-info { padding: 0.15rem 0.6rem 0.4rem 0.15rem; display: flex; flex-direction: column; justify-content: space-between; flex: 1; min-width: 0; }
	.c-mid { display: flex; align-items: center; justify-content: space-between; gap: 0.4rem; }

	/* ===== HORIZONTAL (1024+) — scales in 2 tiers ===== */

	/* -- Medium tier: MacBook (1024–1599) -- */
	.h-image { width: 160px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; padding: 0.5rem; }
	.h-body { padding: 0.6rem 1rem; display: flex; flex-direction: column; justify-content: space-between; flex: 1; min-width: 0; }
	.h-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 0.5rem; }
	.h-title { font-family: 'DM Serif Display', serif; font-size: 1.1rem; line-height: 1.25; color: #2c1810; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.h-country { font-family: 'DM Sans', sans-serif; font-size: 0.8rem; color: #8c7b6b; font-weight: 400; margin-left: 0.2rem; }
	.h-roastery { font-size: 0.78rem; color: #8c7b6b; margin-top: 0.15rem; }
	.h-mid { display: flex; align-items: center; justify-content: space-between; gap: 1rem; margin-top: 0.4rem; }

	/* -- Large tier: Mac Mini (1600+) -- */
	@media (min-width: 1600px) {
		.h-image { width: 300px; padding: 1rem; }
		.h-body { padding: 1.25rem 1.5rem; }
		.h-title { font-size: 1.5rem; }
		.h-country { font-size: 0.9rem; margin-left: 0.25rem; }
		.h-roastery { font-size: 0.9rem; margin-top: 0.25rem; }
		.h-mid { gap: 1.5rem; margin-top: 0.75rem; }
	}

	/* ===== SHARED: taste bars ===== */
	.taste-col { display: flex; flex-direction: column; gap: 0.2rem; flex: 1; min-width: 0; }

	.taste-item { display: flex; align-items: center; gap: 0.3rem; }
	.taste-lbl { font-size: 0.6rem; color: #8c7b6b; text-transform: uppercase; letter-spacing: 0.03em; width: 2.5rem; flex-shrink: 0; }
	.taste-lbl.ts { font-size: 0.5rem; width: 1.8rem; }
	.taste-bg { width: 60px; height: 5px; background: var(--color-card-inset); border-radius: 3px; overflow: hidden; }
	.taste-bg.ts { width: 40px; height: 3px; border-radius: 2px; }
	.taste-fill { height: 100%; background: linear-gradient(90deg, #d4a574, #b45309); border-radius: inherit; }
	.taste-num { font-size: 0.65rem; font-weight: 600; color: #92400e; width: 0.9rem; text-align: right; flex-shrink: 0; }
	.taste-num.ts { font-size: 0.5rem; width: 0.7rem; }

	@media (min-width: 1600px) {
		.taste-col { gap: 0.4rem; }
		.taste-lbl { font-size: 0.65rem; width: 2.8rem; }
		.taste-bg { width: 80px; height: 6px; }
		.taste-num { font-size: 0.7rem; width: 1rem; }
	}

	/* ===== SHARED: metrics ===== */
	.met-col { display: grid; grid-template-columns: 1fr; gap: 0.2rem; flex-shrink: 0; }
	.met { display: grid; grid-template-columns: auto 1fr; align-items: center; gap: 0.6rem; background: var(--color-card-inset); padding: 0.15rem 0.7rem; border-radius: 0.4rem; min-width: 5rem; }
	.met.ms { gap: 0.45rem; padding: 0.12rem 0.55rem; border-radius: 0.35rem; min-width: 4.2rem; }
	.met-ico { opacity: 0.5; width: 20px; height: 20px; }
	.met-ico.mis { width: 18px; height: 18px; }
	:global(.met-val) { font-weight: 700; color: #92400e; font-size: 1.2rem; text-align: right; }
	:global(.met-val.mvs) { font-size: 1.1rem; }
	.met-price { font-weight: 700; color: #b45309; font-size: 1.2rem; text-align: right; }
	.met-price.mps { font-size: 1.1rem; }

	@media (min-width: 1600px) {
		.met-col { gap: 0.3rem; }
		.met { gap: 0.75rem; padding: 0.25rem 0.9rem; border-radius: 0.5rem; min-width: 6rem; }
		.met-ico { width: 28px; height: 28px; }
		:global(.met-val) { font-size: 1.7rem; }
		.met-price { font-size: 1.7rem; }
	}

	/* ===== SHARED: descriptors ===== */
	.desc-row { display: flex; align-items: center; gap: 0.3rem; flex-wrap: wrap; margin-top: 0.3rem; }
	.desc-row.ds { margin-top: 0.2rem; }
	.desc { font-size: 0.7rem; padding: 0.15rem 0.45rem; border-radius: 0.25rem; background: transparent; border: 1px solid #d4c9b8; color: #8c7b6b; white-space: nowrap; }
	.desc.ds { font-size: 0.6rem; padding: 0.1rem 0.35rem; border-radius: 0.2rem; }

	@media (min-width: 1600px) {
		.desc-row { gap: 0.35rem; margin-top: auto; padding-top: 0.75rem; }
		.desc { font-size: 0.75rem; padding: 0.2rem 0.55rem; border-radius: 0.3rem; }
	}

	/* ===== SHARED: badges & flag ===== */
	.flag { margin-right: 0.15rem; }
	@media (min-width: 1600px) { .flag { margin-right: 0.3rem; } }

	.badge { font-size: 0.6rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; padding: 0.12rem 0.4rem; border-radius: 999px; white-space: nowrap; flex-shrink: 0; }
	.badge-sm { font-size: 0.55rem; padding: 0.1rem 0.35rem; }
	.badge-open { background: #dcfce7; color: #166534; }
	.badge-store { background: #dbeafe; color: #1e40af; }
	@media (min-width: 1600px) { .badge { font-size: 0.65rem; padding: 0.15rem 0.5rem; } }
</style>
