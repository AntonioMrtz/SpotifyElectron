import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import Language from './languages';

interface Translations {
  startMenu: Record<string, string>;
  registerMenu: Record<string, string>;
  commonPopover: Record<string, string>;
  contextMenuProfile: Record<string, string>;
}

const loadTranslationFiles = async (): Promise<
  Record<string, Translations>
> => {
  const languages = ['en', 'es']; // Use 'as const' to infer literal types
  const translations: Record<string, Translations> = {};

  const translationPromises = languages.map(async (lang) => {
    translations[lang] = {
      startMenu: await import(`./localization/${lang}/start-menu.json`),
      registerMenu: await import(`./localization/${lang}/register-menu.json`),
      commonPopover: await import(`./localization/${lang}/common-popover.json`),
      contextMenuProfile: await import(
        `./localization/${lang}/context-menu-profile.json`
      ),
    };
  });

  await Promise.all(translationPromises);

  return translations;
};

export const initializeI18n = async () => {
  const resources = await loadTranslationFiles();

  i18n.use(initReactI18next).init({
    resources: {
      en: {
        translation: resources.en,
      },
      es: {
        translation: resources.es,
      },
    },
    lng: 'en',
    fallbackLng: 'es',
    interpolation: {
      escapeValue: false,
    },
  });
};

// eslint-disable-next-line import/prefer-default-export
export const changeLanguage = (language: Language) => {
  i18n.changeLanguage(language);
};
