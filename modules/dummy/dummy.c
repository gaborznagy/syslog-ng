#include "dummy.h"
#include "dummy-parser.h"

#include "plugin.h"
#include "messages.h"
#include "misc.h"
#include "stats/stats-registry.h"
#include "logqueue.h"
#include "driver.h"
#include "plugin-types.h"
#include "logthrdest/logthrdestdrv.h"


typedef struct
{
  LogThreadedDestDriver super;

  gchar *filename;
} DummyDriver;

/*
 * Configuration
 */

void
dummy_dd_set_filename(LogDriver *d, const gchar *filename)
{
  DummyDriver *self = (DummyDriver *)d;

  g_free(self->filename);
  self->filename = g_strdup(filename);
}

/*
 * Utilities
 */

static const gchar *
dummy_dd_format_stats_instance(LogThreadedDestDriver *d)
{
  DummyDriver *self = (DummyDriver *)d;
  static gchar persist_name[1024];

  g_snprintf(persist_name, sizeof(persist_name),
             "dummy,%s", self->filename);
  return persist_name;
}

static const gchar *
dummy_dd_format_persist_name(const LogPipe *d)
{
  DummyDriver *self = (DummyDriver *)d;
  static gchar persist_name[1024];

  if (d->persist_name)
    g_snprintf(persist_name, sizeof(persist_name), "dummy.%s", d->persist_name);
  else
    g_snprintf(persist_name, sizeof(persist_name), "dummy.%s", self->filename);

  return persist_name;
}

static gboolean
dummy_dd_connect(DummyDriver *self, gboolean reconnect)
{
  msg_debug("Dummy connection succeeded",
            evt_tag_str("driver", self->super.super.super.id), NULL);

  return TRUE;
}

static void
dummy_dd_disconnect(LogThreadedDestDriver *d)
{
  DummyDriver *self = (DummyDriver *)d;

  msg_debug("Dummy connection closed",
            evt_tag_str("driver", self->super.super.super.id), NULL);
}

/*
 * Worker thread
 */

static LogThreadedResult
dummy_worker_insert(LogThreadedDestDriver *d, LogMessage *msg)
{
  DummyDriver *self = (DummyDriver *)d;

  msg_debug("Dummy message sent",
            evt_tag_str("driver", self->super.super.super.id),
            evt_tag_str("filename", self->filename),
            NULL);

  return LTR_SUCCESS;
  /*
   * LTR_DROP,
   * LTR_ERROR,
   * LTR_SUCCESS,
   * LTR_QUEUED,
   * LTR_NOT_CONNECTED,
   * LTR_RETRY,
  */
}

static void
dummy_worker_thread_init(LogThreadedDestDriver *d)
{
  DummyDriver *self = (DummyDriver *)d;

  msg_debug("Worker thread started",
            evt_tag_str("driver", self->super.super.super.id),
            NULL);

  dummy_dd_connect(self, FALSE);
}

static void
dummy_worker_thread_deinit(LogThreadedDestDriver *d)
{
  DummyDriver *self = (DummyDriver *)d;

  msg_debug("Worker thread stopped",
            evt_tag_str("driver", self->super.super.super.id),
            NULL);
}

/*
 * Main thread
 */

static gboolean
dummy_dd_init(LogPipe *d)
{
  DummyDriver *self = (DummyDriver *)d;
  GlobalConfig *cfg = log_pipe_get_config(d);

  if (!log_threaded_dest_driver_init_method(d))
    return FALSE;

  msg_verbose("Initializing Dummy destination",
              evt_tag_str("driver", self->super.super.super.id),
              evt_tag_str("filename", self->filename),
              NULL);

  return log_threaded_dest_driver_start_workers(&self->super);
}

static void
dummy_dd_free(LogPipe *d)
{
  DummyDriver *self = (DummyDriver *)d;

  g_free(self->filename);

  log_threaded_dest_driver_free(d);
}

/*
 * Plugin glue.
 */

LogDriver *
dummy_dd_new(GlobalConfig *cfg)
{
  DummyDriver *self = g_new0(DummyDriver, 1);

  log_threaded_dest_driver_init_instance(&self->super, cfg);
  self->super.super.super.super.init = dummy_dd_init;
  self->super.super.super.super.free_fn = dummy_dd_free;

  self->super.worker.thread_init = dummy_worker_thread_init;
  self->super.worker.thread_deinit = dummy_worker_thread_deinit;
  self->super.worker.disconnect = dummy_dd_disconnect;
  self->super.worker.insert = dummy_worker_insert;

  self->super.format_stats_instance = dummy_dd_format_stats_instance;
  self->super.super.super.super.generate_persist_name = dummy_dd_format_persist_name;
  //self->super.stats_source = SCS_DUMMY;

  return (LogDriver *)self;
}

extern CfgParser dummy_parser;

static Plugin dummy_plugin =
{
  .type = LL_CONTEXT_DESTINATION,
  .name = "dummy",
  .parser = &dummy_parser,
};

gboolean
dummy_module_init(PluginContext *context, CfgArgs *args)
{
  plugin_register(context, &dummy_plugin, 1);

  return TRUE;
}

const ModuleInfo module_info =
{
  .canonical_name = "dummy",
  .version = SYSLOG_NG_VERSION,
  .description = "This is a dummy destination for syslog-ng.",
  .core_revision = SYSLOG_NG_SOURCE_REVISION,
  .plugins = &dummy_plugin,
  .plugins_len = 1,
};
