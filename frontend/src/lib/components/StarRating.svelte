<script lang="ts">
	let { rating = 0, interactive = false, onRate }: {
		rating: number;
		interactive?: boolean;
		onRate?: (value: number) => void;
	} = $props();

	let hoverRating = $state(0);

	function handleClick(value: number) {
		if (interactive && onRate) {
			onRate(value);
		}
	}

	function displayRating(starIndex: number, currentRating: number): 'full' | 'half' | 'empty' {
		const value = currentRating / 2; // e.g. 7 → 3.5
		const fullStars = Math.floor(value); // e.g. 3
		const hasHalf = value % 1 !== 0; // e.g. true
		if (starIndex <= fullStars) return 'full';
		if (hasHalf && starIndex === fullStars + 1) return 'half';
		return 'empty';
	}
</script>

<div class="flex items-center gap-0.5" role={interactive ? 'radiogroup' : 'img'} aria-label={`Rating: ${rating / 2} out of 5 stars`}>
	{#each [1, 2, 3, 4, 5] as star}
		{@const fill = displayRating(star, hoverRating || rating)}
		{#if interactive}
			<button
				type="button"
				class="relative w-6 h-6 cursor-pointer group"
				onmouseenter={() => hoverRating = star * 2}
				onmouseleave={() => hoverRating = 0}
				onclick={(e) => {
					const rect = (e.currentTarget as HTMLElement).getBoundingClientRect();
					const isLeft = e.clientX - rect.left < rect.width / 2;
					handleClick(isLeft ? star * 2 - 1 : star * 2);
				}}
			>
				<svg viewBox="0 0 24 24" class="w-6 h-6 transition-colors {fill === 'full' ? 'text-amber-400' : fill === 'half' ? 'text-amber-400' : 'text-stone-300 group-hover:text-amber-200'}">
					{#if fill === 'half'}
						<defs>
							<linearGradient id="half-{star}">
								<stop offset="50%" stop-color="currentColor" />
								<stop offset="50%" stop-color="#d6d3d1" />
							</linearGradient>
						</defs>
						<path fill="url(#half-{star})" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
					{:else}
						<path fill="currentColor" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
					{/if}
				</svg>
			</button>
		{:else}
			<svg viewBox="0 0 24 24" class="w-5 h-5 {fill === 'full' ? 'text-amber-400' : fill === 'half' ? 'text-amber-400' : 'text-stone-300'}">
				{#if fill === 'half'}
					<defs>
						<linearGradient id="half-display-{star}">
							<stop offset="50%" stop-color="currentColor" />
							<stop offset="50%" stop-color="#d6d3d1" />
						</linearGradient>
					</defs>
					<path fill="url(#half-display-{star})" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
				{:else}
					<path fill="currentColor" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
				{/if}
			</svg>
		{/if}
	{/each}
</div>
