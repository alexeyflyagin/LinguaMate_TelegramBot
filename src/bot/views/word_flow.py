from aiogram.enums import ParseMode

from src.bot.resourses.strings import sres
from src.bot.resourses.strings.utils import esc_md
from src.bot.views.keyboards.word_flow import word_flow_im, word_flow_about_im
from src.bot.views.models.general import View, ViewType
from src.bot.views.models.word_flow import WordFlowViewData, WordFlowAboutViewData


def word_flow__view(data: WordFlowViewData) -> View:
    word = esc_md(data.word)
    return View(
        view_type=ViewType.TEXT,
        text=sres.DICTIONARY.WORD_FLOW.WORD.format(word=word),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=word_flow_im(data.id)
    )


def word_flow_about__view(data: WordFlowAboutViewData) -> View:
    escape_translations = []
    for translation in data.word.translations:
        escape_translations.append(sres.DICTIONARY.WORD_FLOW.WORD_TRANSLATE.format(translation=esc_md(translation)))
    translations = ', '.join(escape_translations)
    word = esc_md(data.word.word)
    return View(
        view_type=ViewType.TEXT,
        text=sres.DICTIONARY.WORD_FLOW.ABOUT.format(word=word, translations=translations),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=word_flow_about_im(data.word.id)
    )
