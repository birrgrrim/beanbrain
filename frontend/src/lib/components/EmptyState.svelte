<script lang="ts">
	let { img, title, subtitle }: {
		img: string;
		title: string;
		subtitle?: string;
	} = $props();
</script>

<div class="flex flex-col items-center justify-center h-full text-center">
	<div class="rounded-full bg-parchment p-8 mb-4"
		style="box-shadow: 0 0 40px 20px var(--color-parchment);">
		<img src="/img/{img}" alt="" class="opacity-70" style="max-width: 220px;" />
	</div>
	<p class="text-stone-500 text-2xl" style="font-family: 'DM Serif Display', serif;">{title}</p>
	{#if subtitle}<p class="text-stone-400 text-base mt-2">{subtitle}</p>{/if}
</div>
