<script lang="ts">
	let { rating = 0, interactive = false, onRate, size }: {
		rating: number;
		interactive?: boolean;
		onRate?: (value: number) => void;
		size?: 'sm' | 'md' | 'lg' | 'xl';
	} = $props();

	// Default: xl for interactive (easier to tap half-beans), md for display
	const effectiveSize = size ?? (interactive ? 'xl' : 'md');

	let hoverRating = $state(0);

	function handleClick(value: number) {
		if (interactive && onRate) {
			onRate(value);
		}
	}

	function getValueFromEvent(e: MouseEvent, beanIndex: number): number {
		const rect = (e.currentTarget as HTMLElement).getBoundingClientRect();
		const isLeft = e.clientX - rect.left < rect.width / 2;
		return isLeft ? beanIndex * 2 - 1 : beanIndex * 2;
	}

	function beanType(beanIndex: number, currentRating: number): 'full' | 'half' | 'empty' {
		const value = currentRating / 2;
		const fullBeans = Math.floor(value);
		const hasHalf = value % 1 !== 0;
		if (beanIndex <= fullBeans) return 'full';
		if (hasHalf && beanIndex === fullBeans + 1) return 'half';
		return 'empty';
	}

	const beanSrc: Record<string, string> = {
		full: '/img/bean-full.png',
		half: '/img/bean-half.png',
		empty: '/img/bean-empty.png',
	};

	// width in px — height is 1.4x width (bean aspect ratio)
	const sizeMap: Record<string, number> = {
		sm: 10,
		md: 14,
		lg: 18,
		xl: 28,
	};
</script>

<div class="inline-flex items-center gap-1" role={interactive ? 'radiogroup' : 'img'} aria-label={`Rating: ${rating / 2} out of 5`}>
	{#each [1, 2, 3, 4, 5] as bean}
		{@const type = beanType(bean, hoverRating || rating)}
		{@const px = sizeMap[effectiveSize]}
		{#if interactive}
			<button
				type="button"
				class="cursor-pointer transition-transform hover:scale-110"
				style="width: {px}px; height: {Math.round(px * 1.4)}px;"
				onmousemove={(e) => hoverRating = getValueFromEvent(e, bean)}
				onmouseleave={() => hoverRating = 0}
				onclick={(e) => handleClick(getValueFromEvent(e, bean))}
			>
				<img src={beanSrc[type]} alt="" style="width: {px}px; height: {Math.round(px * 1.4)}px;"
					class="transition-opacity {type === 'empty' ? 'opacity-40' : 'opacity-90'}" />
			</button>
		{:else}
			<img src={beanSrc[type]} alt="" style="width: {px}px; height: {Math.round(px * 1.4)}px;"
				class="{type === 'empty' ? 'opacity-30' : 'opacity-80'}" />
		{/if}
	{/each}
</div>
