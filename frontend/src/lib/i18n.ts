import { derived } from 'svelte/store';
import { lang } from './lang';

const translations: Record<string, Record<string, string>> = {
	// Top bar & tabs
	'tab.coffee': { en: 'Coffee', uk: 'Кава' },
	'tab.grinders': { en: 'Grinders', uk: 'Кавомолки' },
	'tab.persons': { en: 'Persons', uk: 'Персони' },

	// Coffee sidebar
	'sidebar.search': { en: 'Search coffees...', uk: 'Пошук кави...' },
	'sidebar.empty': { en: 'No coffees yet', uk: 'Кави ще немає' },
	'sidebar.no_matches': { en: 'No matches', uk: 'Нічого не знайдено' },

	// Empty state
	'empty.title': { en: 'Select a coffee', uk: 'Оберіть каву' },
	'empty.subtitle': { en: 'or add a new one to get started', uk: 'або додайте нову' },

	// Coffee detail
	'detail.origin': { en: 'Origin', uk: 'Країна' },
	'detail.process': { en: 'Process', uk: 'Обробка' },
	'detail.roast': { en: 'Roast', uk: 'Обсмаження' },
	'detail.score': { en: 'Score', uk: 'Оцінка' },
	'detail.sweet': { en: 'Sweet', uk: 'Солодкість' },
	'detail.acid': { en: 'Acid', uk: 'Кислотність' },
	'detail.bitter': { en: 'Bitter', uk: 'Гіркота' },
	'detail.flavor_profile': { en: 'Flavor profile', uk: 'Профіль смаку' },
	'detail.roastery_link': { en: 'View on roastery site', uk: 'Переглянути на сайті' },
	'detail.delete': { en: 'Delete', uk: 'Видалити' },
	'detail.delete_confirm': { en: 'Delete this coffee and all its tastings?', uk: 'Видалити цю каву та всі дегустації?' },

	// Grinder settings
	'grinder.title': { en: 'Grinder Setting', uk: 'Налаштування помолу' },
	'grinder.add': { en: '+ Add', uk: '+ Додати' },
	'grinder.no_setting': { en: 'No setting recorded yet', uk: 'Ще немає налаштувань' },
	'grinder.setting': { en: 'Setting', uk: 'Помол' },
	'grinder.basket': { en: 'Basket', uk: 'Кошик' },
	'grinder.notes': { en: 'Notes', uk: 'Нотатки' },
	'grinder.save': { en: 'Save', uk: 'Зберегти' },
	'grinder.cancel': { en: 'Cancel', uk: 'Скасувати' },

	// Reviews
	'tasting.title': { en: 'Reviews', uk: 'Відгуки' },
	'tasting.add': { en: '+ Add Review', uk: '+ Додати відгук' },
	'tasting.empty': { en: 'No reviews yet', uk: 'Ще немає відгуків' },
	'tasting.who': { en: "Who's reviewing?", uk: 'Хто оцінює?' },
	'tasting.select': { en: 'Select person...', uk: 'Оберіть персону...' },
	'tasting.no_tasters': { en: 'Add persons in Persons tab first', uk: 'Спочатку додайте персону' },
	'tasting.rating': { en: 'Rating', uk: 'Оцінка' },
	'tasting.comment': { en: 'Comment', uk: 'Коментар' },
	'tasting.comment_placeholder': { en: 'What did you taste?', uk: 'Що ви відчули?' },
	'tasting.flavors': { en: 'Flavors you taste', uk: 'Смаки які ви відчуваєте' },
	'tasting.save': { en: 'Save Review', uk: 'Зберегти відгук' },
	'tasting.cancel': { en: 'Cancel', uk: 'Скасувати' },

	// Add coffee
	'add.title': { en: 'Add Coffee', uk: 'Додати каву' },
	'add.url_hint': { en: 'Paste a roastery URL to auto-fill', uk: 'Вставте посилання для автозаповнення' },
	'add.fetch': { en: 'Fetch', uk: 'Завантажити' },
	'add.fetching': { en: 'Fetching...', uk: 'Завантаження...' },
	'add.name': { en: 'Name', uk: 'Назва' },
	'add.roastery': { en: 'Roastery', uk: 'Обсмажувач' },
	'add.origin': { en: 'Origin', uk: 'Країна' },
	'add.process': { en: 'Process', uk: 'Обробка' },
	'add.roast_level': { en: 'Roast Level', uk: 'Рівень обсмаження' },
	'add.notes': { en: 'Notes', uk: 'Нотатки' },
	'add.descriptors': { en: 'Roastery Descriptors', uk: 'Дескриптори обсмажувача' },
	'add.save': { en: 'Add Coffee', uk: 'Додати каву' },
	'add.saving': { en: 'Saving...', uk: 'Збереження...' },
	'add.cancel': { en: 'Cancel', uk: 'Скасувати' },

	// Descriptor autocomplete
	'desc.search': { en: 'Search flavors...', uk: 'Пошук смаків...' },
	'desc.suggested': { en: 'Roastery suggests', uk: 'Обсмажувач рекомендує' },

	// Persons panel
	'persons.title': { en: 'Persons', uk: 'Персони' },
	'persons.subtitle': { en: "Who's tasting coffee", uk: 'Хто дегустує каву' },
	'persons.empty': { en: 'No tasters yet — add yourself!', uk: 'Ще немає дегустаторів — додайте себе!' },
	'persons.add_placeholder': { en: 'Add person...', uk: 'Додати персону...' },
	'persons.add': { en: 'Add', uk: 'Додати' },

	// Grinders panel
	'grinders.title': { en: 'Grinders & Equipment', uk: 'Кавомолки та обладнання' },
	'grinders.grinders': { en: 'Grinders', uk: 'Кавомолки' },
	'grinders.machines': { en: 'Espresso Machines', uk: 'Еспресо машини' },
	'grinders.brew_methods': { en: 'Brew Methods', uk: 'Методи приготування' },
	'grinders.baskets': { en: 'Basket Sizes', uk: 'Розміри кошиків' },

	// Common
	'common.optional': { en: 'Optional', uk: 'Необов\'язково' },
};

export const t = derived(lang, ($lang) => {
	return (key: string): string => {
		const entry = translations[key];
		if (!entry) return key;
		return entry[$lang] || entry['en'] || key;
	};
});
