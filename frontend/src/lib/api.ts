const BASE_URL = '/api';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
	const res = await fetch(`${BASE_URL}${path}`, {
		headers: { 'Content-Type': 'application/json' },
		...options,
	});
	if (!res.ok) {
		let detail = `${res.status} ${res.statusText}`;
		try {
			const body = await res.json();
			if (body.detail) detail = body.detail;
		} catch { /* no JSON body */ }
		throw new Error(detail);
	}
	if (res.status === 204) return undefined as T;
	return res.json();
}

export interface Descriptor {
	id: number;
	name: string;
	category: string;
}

export interface Taster {
	id: number;
	name: string;
	avatar: string | null;
}

export interface Grinder {
	id: number;
	manufacturer: string;
	model: string | null;
	kind: string;
	avatar: string | null;
	range_min: number;
	range_max: number | null;
	step: number;
}

export interface BrewSetup {
	id: number;
	method_type: string;
	manufacturer: string;
	model: string | null;
	basket_grams: number | null;
	avatar: string | null;
}

export interface BrewMethodType {
	key: string;
	icon: string;
	has_basket: boolean;
}

export interface GrinderSetting {
	id: number;
	coffee_id: number;
	grinder_id: number;
	brew_setup_id: number;
	setting: number;
	notes: string | null;
	grinder: Grinder;
	brew_setup: BrewSetup;
}

export interface Review {
	id: number;
	coffee_id: number;
	taster_id: number;
	brew_setup_id: number;
	taster: Taster;
	brew_setup: BrewSetup;
	rating: number;
	comment: string | null;
	updated_at: string;
	descriptors: Descriptor[];
}

export interface Origin {
	id: number;
	name_en: string;
	name_uk: string;
	flag: string | null;
}

export interface Roastery {
	id: number;
	name: string;
	website: string | null;
	logo_url: string | null;
	is_active: boolean;
}

export interface Coffee {
	id: number;
	name: string;
	roastery_id: number;
	origin_id: number | null;
	roastery_ref: Roastery;
	origin_ref: Origin | null;
	process: string | null;
	roast_level: string | null;
	roastery_url: string | null;
	image_url: string | null;
	score: number | null; // float, e.g. 83.5
	sweetness: number | null;
	acidity: number | null;
	bitterness: number | null;
	notes: string | null;
	roaster_comment: Record<string, string> | null;
	price: number | null;
	price_wholesale: number | null;
	in_stock: boolean;
	in_store: boolean;
	created_at: string;
	updated_at: string | null;
	fetched_at: string | null;
	roastery_descriptors: Descriptor[];
	reviews: Review[];
	grinder_settings: GrinderSetting[];
}

export interface CoffeeListItem {
	id: number;
	name: string;
	roastery_id: number;
	origin_id: number | null;
	roastery_ref: Roastery;
	origin_ref: Origin | null;
	roast_level: string | null;
	image_url: string | null;
	score: number | null;
	sweetness: number | null;
	acidity: number | null;
	bitterness: number | null;
	price: number | null;
	price_wholesale: number | null;
	in_stock: boolean;
	in_store: boolean;
	avg_rating: number | null;
	person_rating: number | null;
	default_grind: number | null;
	default_grind_step: number;
	created_at: string;
	roastery_descriptors: Descriptor[];
}

export interface ScrapeResult {
	name: string;
	roastery: string;
	origin: string | null;
	process: string | null;
	roast_level: string | null;
	roastery_url: string;
	image_url: string | null;
	score: number | null; // float, e.g. 83.5
	sweetness: number | null;
	acidity: number | null;
	bitterness: number | null;
	price: number | null;
	price_wholesale: number | null;
	flavor_descriptors: Record<string, string[]>;
	name_i18n: Record<string, string>;
	roaster_comment: Record<string, string>;
}

export const BREW_METHOD_TYPES: BrewMethodType[] = [
	{ key: 'espresso', icon: 'method-espresso.png', has_basket: true },
	{ key: 'pourover', icon: 'method-pourover.png', has_basket: false },
	{ key: 'aeropress', icon: 'method-aeropress.png', has_basket: false },
	{ key: 'frenchpress', icon: 'method-frenchpress.png', has_basket: false },
	{ key: 'moka', icon: 'method-moka.png', has_basket: false },
	{ key: 'cezve', icon: 'method-cezve.png', has_basket: false },
];

export const api = {
	coffees: {
		list: (opts?: { search?: string; tasterId?: number | null; grinderId?: number | null; brewSetupId?: number | null }) => {
			const params = new URLSearchParams();
			if (opts?.search) params.set('search', opts.search);
			if (opts?.tasterId) params.set('taster_id', String(opts.tasterId));
			if (opts?.grinderId) params.set('grinder_id', String(opts.grinderId));
			if (opts?.brewSetupId) params.set('brew_setup_id', String(opts.brewSetupId));
			const qs = params.toString();
			return request<CoffeeListItem[]>(`/coffees/${qs ? `?${qs}` : ''}`);
		},
		get: (id: number) => request<Coffee>(`/coffees/${id}`),
		create: (data: {
			name: string;
			roastery_id: number;
			origin_id?: number | null;
			process?: string;
			roast_level?: string;
			roastery_url?: string;
			image_url?: string;
			score?: number;
			sweetness?: number;
			acidity?: number;
			bitterness?: number;
			notes?: string;
			roaster_comment?: Record<string, string>;
			price?: number;
			price_wholesale?: number;
			in_stock?: boolean;
			in_store?: boolean;
			roastery_descriptor_ids?: number[];
		}) => request<Coffee>('/coffees/', { method: 'POST', body: JSON.stringify(data) }),
		update: (id: number, data: Record<string, unknown>) =>
			request<Coffee>(`/coffees/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
		delete: (id: number) => request<void>(`/coffees/${id}`, { method: 'DELETE' }),
		refresh: (id: number) => request<Coffee>(`/coffees/${id}/refresh`, { method: 'POST' }),
	},
	reviews: {
		upsert: (coffeeId: number, data: {
			taster_id: number;
			brew_setup_id: number;
			rating: number;
			comment?: string;
			descriptor_ids?: number[];
		}) => request<Review>(`/coffees/${coffeeId}/reviews/`, {
			method: 'PUT', body: JSON.stringify(data),
		}),
		delete: (coffeeId: number, reviewId: number) =>
			request<void>(`/coffees/${coffeeId}/reviews/${reviewId}`, { method: 'DELETE' }),
	},
	grinderSettings: {
		create: (coffeeId: number, data: {
			grinder_id: number;
			brew_setup_id: number;
			setting: number;
			notes?: string;
		}) => request<GrinderSetting>(`/coffees/${coffeeId}/settings/`, {
			method: 'POST', body: JSON.stringify(data),
		}),
		delete: (coffeeId: number, settingId: number) =>
			request<void>(`/coffees/${coffeeId}/settings/${settingId}`, { method: 'DELETE' }),
	},
	tasters: {
		list: () => request<Taster[]>('/tasters/'),
		create: (name: string) => request<Taster>('/tasters/', {
			method: 'POST', body: JSON.stringify({ name }),
		}),
		update: (id: number, data: { name: string; avatar?: string | null }) =>
			request<Taster>(`/tasters/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
		delete: (id: number) => request<void>(`/tasters/${id}`, { method: 'DELETE' }),
		dependents: (id: number) => request<{ reviews: number }>(`/tasters/${id}/dependents`),
	},
	descriptors: {
		list: () => request<Descriptor[]>('/descriptors/'),
	},
	grinders: {
		list: () => request<Grinder[]>('/grinders/'),
		create: (data: { manufacturer: string; model?: string; kind?: string; is_default?: boolean; range_min?: number; range_max?: number | null; step?: number }) =>
			request<Grinder>('/grinders/', { method: 'POST', body: JSON.stringify(data) }),
		update: (id: number, data: Record<string, unknown>) =>
			request<Grinder>(`/grinders/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
		delete: (id: number) => request<void>(`/grinders/${id}`, { method: 'DELETE' }),
		dependents: (id: number) => request<{ grinder_settings: number }>(`/grinders/${id}/dependents`),
	},
	brewSetups: {
		list: () => request<BrewSetup[]>('/brew-setups/'),
		create: (data: { method_type: string; manufacturer: string; model?: string; basket_grams?: number; is_default?: boolean }) =>
			request<BrewSetup>('/brew-setups/', { method: 'POST', body: JSON.stringify(data) }),
		update: (id: number, data: Record<string, unknown>) =>
			request<BrewSetup>(`/brew-setups/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
		delete: (id: number) => request<void>(`/brew-setups/${id}`, { method: 'DELETE' }),
		dependents: (id: number) => request<{ grinder_settings: number; reviews: number }>(`/brew-setups/${id}/dependents`),
	},
	brewMethodTypes: {
		list: () => request<BrewMethodType[]>('/brew-method-types'),
	},
	origins: {
		list: () => request<Origin[]>('/origins/'),
	},
	roasteries: {
		list: () => request<Roastery[]>('/roasteries/'),
		create: (data: { name: string; website?: string; logo_url?: string }) =>
			request<Roastery>('/roasteries/', { method: 'POST', body: JSON.stringify(data) }),
		update: (id: number, data: Record<string, unknown>) =>
			request<Roastery>(`/roasteries/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
		delete: (id: number) => request<void>(`/roasteries/${id}`, { method: 'DELETE' }),
		refresh: (id: number) => request<{ refreshed: number; failed: number; errors: string[] }>(
			`/roasteries/${id}/refresh`, { method: 'POST' }),
	},
	scrape: (url: string) =>
		request<ScrapeResult>(`/scrape/?url=${encodeURIComponent(url)}`),
};
