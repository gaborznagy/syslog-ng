#include "dummy.h"
#include "cfg-parser.h"
#include "dummy-grammar.h" // generated by lexer

extern int dummy_debug;
int dummy_parse(CfgLexer *lexer, LogDriver **instance, gpointer arg);

static CfgLexerKeyword dummy_keywords[] = {
  { "dummy", KW_DUMMY },
  { "filename", KW_FILENAME },
  { NULL }
};

CfgParser dummy_parser =
{
#if SYSLOG_NG_ENABLE_DEBUG
  .debug_flag = &dummy_debug,
#endif
  .name = "dummy",
  .keywords = dummy_keywords,
  .parse = (int (*)(CfgLexer *lexer, gpointer *instance, gpointer)) dummy_parse,
  .cleanup = (void (*)(gpointer)) log_pipe_unref,
};

CFG_PARSER_IMPLEMENT_LEXER_BINDING(dummy_, LogDriver **)
