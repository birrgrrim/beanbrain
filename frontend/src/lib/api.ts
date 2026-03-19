const BASE_URL = 'http://localhost:8000';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
	const res = await fetch(`${BASE_URL}${path}`, {
		headers: { 'Content-Type': 'application/json' },
		...options,
	});
	if (!res.ok) {
		throw new Error(`API error: ${res.status} ${res.statusText}`);
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
}

export interface Grinder {
	id: number;
	name: string;
	model: string | null;
	kind: string;
	is_default: boolean;
}

export interface BrewSetup {
	id: number;
	method_type: string;
	name: string;
	basket_grams: number | null;
	is_default: boolean;
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
	taster: Taster;
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
	score: number | null;
	sweetness: number | null;
	acidity: number | null;
	bitterness: number | null;
	notes: string | null;
	roaster_comment: Record<string, string> | null;
	is_available: boolean;
	created_at: string;
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
	is_available: boolean;
	avg_rating: number | null;
	person_rating: number | null;
	default_grind: number | null;
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
	score: number | null;
	sweetness: number | null;
	acidity: number | null;
	bitterness: number | null;
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
		list: (search?: string, tasterId?: number | null) => {
			const params = new URLSearchParams();
			if (search) params.set('search', search);
			if (tasterId) params.set('taster_id', String(tasterId));
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
			is_available?: boolean;
			roastery_descriptor_ids?: number[];
		}) => request<Coffee>('/coffees/', { method: 'POST', body: JSON.stringify(data) }),
		update: (id: number, data: Record<string, unknown>) =>
			request<Coffee>(`/coffees/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
		delete: (id: number) => request<void>(`/coffees/${id}`, { method: 'DELETE' }),
	},
	reviews: {
		upsert: (coffeeId: number, data: {
			taster_id: number;
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
		delete: (id: number) => request<void>(`/tasters/${id}`, { method: 'DELETE' }),
	},
	descriptors: {
		list: () => request<Descriptor[]>('/descriptors/'),
	},
	grinders: {
		list: () => request<Grinder[]>('/grinders/'),
		create: (data: { name: string; model?: string; kind?: string; is_default?: boolean }) =>
			request<Grinder>('/grinders/', { method: 'POST', body: JSON.stringify(data) }),
		update: (id: number, data: Record<string, unknown>) =>
			request<Grinder>(`/grinders/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
		delete: (id: number) => request<void>(`/grinders/${id}`, { method: 'DELETE' }),
	},
	brewSetups: {
		list: () => request<BrewSetup[]>('/brew-setups/'),
		create: (data: { method_type: string; name: string; basket_grams?: number; is_default?: boolean }) =>
			request<BrewSetup>('/brew-setups/', { method: 'POST', body: JSON.stringify(data) }),
		update: (id: number, data: Record<string, unknown>) =>
			request<BrewSetup>(`/brew-setups/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
		delete: (id: number) => request<void>(`/brew-setups/${id}`, { method: 'DELETE' }),
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
	},
	scrape: (url: string) =>
		request<ScrapeResult>(`/scrape/?url=${encodeURIComponent(url)}`),
};
