from aiogram.enums import ParseMode

from src.bot import sres
from src.bot.utils import esc_md
from src.bot.views.keyboards.flow_phrase import flow_phrase_im, flow_phrase_about_im
from src.bot.views.models.flow_phrase import FlowPhraseViewData, FlowPhraseAboutViewData
from src.bot.views.models.general import View, ViewType


def flow_phrase__view(data: FlowPhraseViewData) -> View:
    phrase = esc_md(data.phrase)
    return View(
        view_type=ViewType.TEXT,
        text=sres.PHRASE.FLOW_PHRASE.PHRASE.format(phrase=phrase),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=flow_phrase_im(data.id)
    )


def flow_phrase_about__view(data: FlowPhraseAboutViewData) -> View:
    escape_translations = []
    for translation in data.phrase.translations:
        escape_translations.append(sres.PHRASE.FLOW_PHRASE.PHRASE_TRANSLATE.format(translation=esc_md(translation)))
    translations = '\n'.join(escape_translations)
    phrase = esc_md(data.phrase.phrase)
    return View(
        view_type=ViewType.TEXT,
        text=sres.PHRASE.FLOW_PHRASE.ABOUT.format(phrase=phrase, translations=translations),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=flow_phrase_about_im(data.phrase.id)
    )
