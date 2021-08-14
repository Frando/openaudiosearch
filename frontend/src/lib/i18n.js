import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'

i18n
  // detect user language
  // learn more: https://github.com/i18next/i18next-browser-languageDetector
  .use(LanguageDetector)
  // pass the i18n instance to react-i18next.
  .use(initReactI18next)
  // init i18next
  // for all options read: https://www.i18next.com/overview/configuration-options
  .init({
    debug: true,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false // not needed for react as it escapes by default
    },
    resources: {
      en: {
        translation: {
          // here we will place our translations...
        }
      },
      de: {
        translation: {
          slogan: 'Die Suchmaschine für Community Media',
          search: 'Suche',
          by: 'von',
          publishedon: 'Veröffentlicht am',
          play: 'Abspielen',
          options: 'Optionen',
          playthispost: 'Diesen Beitrag abspielen',
          publisher: 'Veröffentlicher',
          creator: 'Urheber',
          publishingdate: 'Veröffentlichungsdatum',
          sourceurl: 'Quell-URL',
          transcript: {
            hide: 'Transcript ausblenden',
            show: 'Transcript einblenden'
          },
          searchForm: {
            placeholder: 'Suche eingeben...'
          },
          more: 'Mehr',
          less: 'Weniger',
          about: 'About',
          imprint: 'Impressum'

        }
      }
    }
  })

export default i18n
