#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)
from cmk.gui.valuespec import Dictionary, DualListChoice, Float, MonitoringState, Tuple

mssql_waittypes = [
    "ABR",
    "ASSEMBLY_LOAD",
    "ASYNC_DISKPOOL_LOCK",
    "ASYNC_IO_COMPLETION",
    "ASYNC_NETWORK_IO",
    "AUDIT_GROUPCACHE_LOCK",
    "AUDIT_LOGINCACHE_LOCK",
    "AUDIT_ON_DEMAND_TARGET_LOCK",
    "AUDIT_XE_SESSION_MGR",
    "BACKUP",
    "BACKUP_OPERATOR",
    "BACKUPBUFFER",
    "BACKUPIO",
    "BACKUPTHREAD",
    "BAD_PAGE_PROCESS",
    "BROKER_CONNECTION_RECEIVE_TASK",
    "BROKER_ENDPOINT_STATE_MUTEX",
    "BROKER_EVENTHANDLER",
    "BROKER_INIT",
    "BROKER_MASTERSTART",
    "BROKER_RECEIVE_WAITFOR",
    "BROKER_REGISTERALLENDPOINTS",
    "BROKER_SERVICE",
    "BROKER_SHUTDOWN",
    "BROKER_TASK_STOP",
    "BROKER_TO_FLUSH",
    "BROKER_TRANSMITTER",
    "BUILTIN_HASHKEY_MUTEX",
    "CHECK_PRINT_RECORD",
    "CHECKPOINT_QUEUE",
    "CHKPT",
    "CLEAR_DB",
    "CLR_AUTO_EVENT",
    "CLR_CRST",
    "CLR_JOIN",
    "CLR_MANUAL_EVENT",
    "CLR_MEMORY_SPY",
    "CLR_MONITOR",
    "CLR_RWLOCK_READER",
    "CLR_RWLOCK_WRITER",
    "CLR_SEMAPHORE",
    "CLR_TASK_START",
    "CLRHOST_STATE_ACCESS",
    "CMEMTHREAD",
    "CXCONSUMER",
    "CXPACKET",
    "CXROWSET_SYNC",
    "DAC_INIT",
    "DBMIRROR_DBM_EVENT",
    "DBMIRROR_DBM_MUTEX",
    "DBMIRROR_EVENTS_QUEUE",
    "DBMIRROR_SEND",
    "DBMIRROR_WORKER_QUEUE",
    "DBMIRRORING_CMD",
    "DEADLOCK_ENUM_MUTEX",
    "DEADLOCK_TASK_SEARCH",
    "DEBUG",
    "DISABLE_VERSIONING",
    "DISKIO_SUSPEND",
    "DISPATCHER_QUEUE_SEMAPHORE",
    "DLL_LOADING_MUTEX",
    "DROPTEMP",
    "DTC",
    "DTC_ABORT_REQUEST",
    "DTC_RESOLVE",
    "DTC_STATE",
    "DTC_TMDOWN_REQUEST",
    "DTC_WAITFOR_OUTCOME",
    "DUMP_LOG_COORDINATOR",
    "DUMPTRIGGER",
    "EC",
    "EE_PMOLOCK",
    "EE_SPECPROC_MAP_INIT",
    "ENABLE_VERSIONING",
    "ERROR_REPORTING_MANAGER",
    "EXCHANGE",
    "EXECSYNC",
    "EXECUTION_PIPE_EVENT_INTERNAL",
    "FAILPOINT",
    "FCB_REPLICA_READ",
    "FCB_REPLICA_WRITE",
    "FS_FC_RWLOCK",
    "FS_GARBAGE_COLLECTOR_SHUTDOWN",
    "FS_HEADER_RWLOCK",
    "FS_LOGTRUNC_RWLOCK",
    "FSA_FORCE_OWN_XACT",
    "FSAGENT",
    "FSTR_CONFIG_MUTEX",
    "FSTR_CONFIG_RWLOCK",
    "FT_COMPROWSET_RWLOCK",
    "FT_IFTS_RWLOCK",
    "FT_IFTS_SCHEDULER_IDLE_WAIT",
    "FT_IFTSHC_MUTEX",
    "FT_IFTSISM_MUTEX",
    "FT_MASTER_MERGE",
    "FT_METADATA_MUTEX",
    "FT_RESTART_CRAWL",
    "FULLTEXT",
    "GUARDIAN",
    "HADR_AG_MUTEX",
    "HADR_AR_CRITICAL_SECTION_ENTRY",
    "HADR_AR_MANAGER_MUTEX",
    "HADR_ARCONTROLLER_NOTIFICATIONS_SUBSCRIBER_LIST",
    "HADR_BACKUP_BULK_LOCK",
    "HADR_BACKUP_QUEUE",
    "HADR_CLUSAPI_CALL",
    "HADR_COMPRESSED_CACHE_SYNC",
    "HADR_DATABASE_FLOW_CONTROL",
    "HADR_DATABASE_VERSIONING_STATE",
    "HADR_DATABASE_WAIT_FOR_RESTART",
    "HADR_DATABASE_WAIT_FOR_TRANSITION_TO_VERSIONING",
    "HADR_DB_COMMAND",
    "HADR_DB_OP_COMPLETION_SYNC",
    "HADR_DB_OP_START_SYNC",
    "HADR_DBR_SUBSCRIBER",
    "HADR_DBR_SUBSCRIBER_FILTER_LIST",
    "HADR_DBSTATECHANGE_SYNC",
    "HADR_FILESTREAM_BLOCK_FLUSH",
    "HADR_FILESTREAM_FILE_CLOSE",
    "HADR_FILESTREAM_FILE_REQUEST",
    "HADR_FILESTREAM_IOMGR",
    "HADR_FILESTREAM_IOMGR_IOCOMPLETION",
    "HADR_FILESTREAM_MANAGER",
    "HADR_GROUP_COMMIT",
    "HADR_LOGCAPTURE_SYNC",
    "HADR_LOGCAPTURE_WAIT",
    "HADR_LOGPROGRESS_SYNC",
    "HADR_NOTIFICATION_DEQUEUE",
    "HADR_NOTIFICATION_WORKER_EXCLUSIVE_ACCESS",
    "HADR_NOTIFICATION_WORKER_STARTUP_SYNC",
    "HADR_NOTIFICATION_WORKER_TERMINATION_SYNC",
    "HADR_PARTNER_SYNC",
    "HADR_READ_ALL_NETWORKS",
    "HADR_RECOVERY_WAIT_FOR_CONNECTION",
    "HADR_RECOVERY_WAIT_FOR_UNDO",
    "HADR_REPLICAINFO_SYNC",
    "HADR_SYNC_COMMIT",
    "HADR_SYNCHRONIZING_THROTTLE",
    "HADR_TDS_LISTENER_SYNC",
    "HADR_TDS_LISTENER_SYNC_PROCESSING",
    "HADR_TIMER_TASK",
    "HADR_TRANSPORT_DBRLIST",
    "HADR_TRANSPORT_FLOW_CONTROL",
    "HADR_TRANSPORT_SESSION",
    "HADR_WORK_POOL",
    "HADR_WORK_QUEUE",
    "HADR_XRF_STACK_ACCESS",
    "HTTP_ENUMERATION",
    "HTTP_START",
    "IMPPROV_IOWAIT",
    "INTERNAL_TESTING",
    "IO_AUDIT_MUTEX",
    "IO_COMPLETION",
    "IO_RETRY",
    "IOAFF_RANGE_QUEUE",
    "KSOURCE_WAKEUP",
    "KTM_ENLISTMENT",
    "KTM_RECOVERY_MANAGER",
    "KTM_RECOVERY_RESOLUTION",
    "LATCH_DT",
    "LATCH_EX",
    "LATCH_KP",
    "LATCH_NL",
    "LATCH_SH",
    "LATCH_UP",
    "LAZYWRITER_SLEEP",
    "LCK_M_BU",
    "LCK_M_BU_ABORT_BLOCKERS",
    "LCK_M_BU_LOW_PRIORITY",
    "LCK_M_IS",
    "LCK_M_IS_ABORT_BLOCKERS",
    "LCK_M_IS_LOW_PRIORITY",
    "LCK_M_IU",
    "LCK_M_IU_ABORT_BLOCKERS",
    "LCK_M_IU_LOW_PRIORITY",
    "LCK_M_IX",
    "LCK_M_IX_ABORT_BLOCKERS",
    "LCK_M_IX_LOW_PRIORITY",
    "LCK_M_RIn_NL",
    "LCK_M_RIn_NL_ABORT_BLOCKERS",
    "LCK_M_RIn_NL_LOW_PRIORITY",
    "LCK_M_RIn_S",
    "LCK_M_RIn_S_ABORT_BLOCKERS",
    "LCK_M_RIn_S_LOW_PRIORITY",
    "LCK_M_RIn_U",
    "LCK_M_RIn_U_ABORT_BLOCKERS",
    "LCK_M_RIn_U_LOW_PRIORITY",
    "LCK_M_RIn_X",
    "LCK_M_RIn_X_ABORT_BLOCKERS",
    "LCK_M_RIn_X_LOW_PRIORITY",
    "LCK_M_RS_S",
    "LCK_M_RS_S_ABORT_BLOCKERS",
    "LCK_M_RS_S_LOW_PRIORITY",
    "LCK_M_RS_U",
    "LCK_M_RS_U_ABORT_BLOCKERS",
    "LCK_M_RS_U_LOW_PRIORITY",
    "LCK_M_RX_S",
    "LCK_M_RX_S_ABORT_BLOCKERS",
    "LCK_M_RX_S_LOW_PRIORITY",
    "LCK_M_RX_U",
    "LCK_M_RX_U_ABORT_BLOCKERS",
    "LCK_M_RX_U_LOW_PRIORITY",
    "LCK_M_RX_X",
    "LCK_M_RX_X_ABORT_BLOCKERS",
    "LCK_M_RX_X_LOW_PRIORITY",
    "LCK_M_S",
    "LCK_M_S_ABORT_BLOCKERS",
    "LCK_M_S_LOW_PRIORITY",
    "LCK_M_SCH_M",
    "LCK_M_SCH_M_ABORT_BLOCKERS",
    "LCK_M_SCH_M_LOW_PRIORITY",
    "LCK_M_SCH_S",
    "LCK_M_SCH_S_ABORT_BLOCKERS",
    "LCK_M_SCH_S_LOW_PRIORITY",
    "LCK_M_SIU",
    "LCK_M_SIU_ABORT_BLOCKERS",
    "LCK_M_SIU_LOW_PRIORITY",
    "LCK_M_SIX",
    "LCK_M_SIX_ABORT_BLOCKERS",
    "LCK_M_SIX_LOW_PRIORITY",
    "LCK_M_U",
    "LCK_M_U_ABORT_BLOCKERS",
    "LCK_M_U_LOW_PRIORITY",
    "LCK_M_UIX",
    "LCK_M_UIX_ABORT_BLOCKERS",
    "LCK_M_UIX_LOW_PRIORITY",
    "LCK_M_X",
    "LCK_M_X_ABORT_BLOCKERS",
    "LCK_M_X_LOW_PRIORITY",
    "LOGBUFFER",
    "LOGGENERATION",
    "LOGMGR",
    "LOGMGR_FLUSH",
    "LOGMGR_QUEUE",
    "LOGMGR_RESERVE_APPEND",
    "LOWFAIL_MEMMGR_QUEUE",
    "MEMORY_ALLOCATION_EXT",
    "MISCELLANEOUS",
    "MSQL_DQ",
    "MSQL_XACT_MGR_MUTEX",
    "MSQL_XACT_MUTEX",
    "MSQL_XP",
    "MSSEARCH",
    "NET_WAITFOR_PACKET",
    "OLEDB",
    "ONDEMAND_TASK_QUEUE",
    "PAGEIOLATCH_DT",
    "PAGEIOLATCH_EX",
    "PAGEIOLATCH_KP",
    "PAGEIOLATCH_NL",
    "PAGEIOLATCH_SH",
    "PAGEIOLATCH_UP",
    "PAGELATCH_DT",
    "PAGELATCH_EX",
    "PAGELATCH_KP",
    "PAGELATCH_NL",
    "PAGELATCH_SH",
    "PAGELATCH_UP",
    "PARALLEL_BACKUP_QUEUE",
    "PREEMPTIVE_ABR",
    "PREEMPTIVE_AUDIT_ACCESS_EVENTLOG",
    "PREEMPTIVE_AUDIT_ACCESS_SECLOG",
    "PREEMPTIVE_CLOSEBACKUPMEDIA",
    "PREEMPTIVE_CLOSEBACKUPTAPE",
    "PREEMPTIVE_CLOSEBACKUPVDIDEVICE",
    "PREEMPTIVE_CLUSAPI_CLUSTERRESOURCECONTROL",
    "PREEMPTIVE_COM_COCREATEINSTANCE",
    "PREEMPTIVE_HADR_LEASE_MECHANISM",
    "PREEMPTIVE_SOSTESTING",
    "PREEMPTIVE_STRESSDRIVER",
    "PREEMPTIVE_TESTING",
    "PREEMPTIVE_XETESTING",
    "PRINT_ROLLBACK_PROGRESS",
    "PWAIT_HADR_CHANGE_NOTIFIER_TERMINATION_SYNC",
    "PWAIT_HADR_CLUSTER_INTEGRATION",
    "PWAIT_HADR_OFFLINE_COMPLETED",
    "PWAIT_HADR_ONLINE_COMPLETED",
    "PWAIT_HADR_POST_ONLINE_COMPLETED",
    "PWAIT_HADR_WORKITEM_COMPLETED",
    "PWAIT_MD_LOGIN_STATS",
    "PWAIT_MD_RELATION_CACHE",
    "PWAIT_MD_SERVER_CACHE",
    "PWAIT_MD_UPGRADE_CONFIG",
    "PWAIT_METADATA_LAZYCACHE_RWLOCk",
    "QPJOB_KILL",
    "QPJOB_WAITFOR_ABORT",
    "QRY_MEM_GRANT_INFO_MUTEX",
    "QUERY_ERRHDL_SERVICE_DONE",
    "QUERY_EXECUTION_INDEX_SORT_EVENT_OPEN",
    "QUERY_NOTIFICATION_MGR_MUTEX",
    "QUERY_NOTIFICATION_SUBSCRIPTION_MUTEX",
    "QUERY_NOTIFICATION_TABLE_MGR_MUTEX",
    "QUERY_NOTIFICATION_UNITTEST_MUTEX",
    "QUERY_OPTIMIZER_PRINT_MUTEX",
    "QUERY_TRACEOUT",
    "QUERY_WAIT_ERRHDL_SERVICE",
    "RECOVER_CHANGEDB",
    "REPL_CACHE_ACCESS",
    "REPL_SCHEMA_ACCESS",
    "REPLICA_WRITES",
    "REQUEST_DISPENSER_PAUSE",
    "REQUEST_FOR_DEADLOCK_SEARCH",
    "RESMGR_THROTTLED",
    "RESOURCE_QUEUE",
    "RESOURCE_SEMAPHORE",
    "RESOURCE_SEMAPHORE_MUTEX",
    "RESOURCE_SEMAPHORE_QUERY_COMPILE",
    "RESOURCE_SEMAPHORE_SMALL_QUERY",
    "SEC_DROP_TEMP_KEY",
    "SECURITY_MUTEX",
    "SEQUENTIAL_GUID",
    "SERVER_IDLE_CHECK",
    "SHUTDOWN",
    "SLEEP_BPOOL_FLUSH",
    "SLEEP_DBSTARTUP",
    "SLEEP_DCOMSTARTUP",
    "SLEEP_MSDBSTARTUP",
    "SLEEP_SYSTEMTASK",
    "SLEEP_TASK",
    "SLEEP_TEMPDBSTARTUP",
    "SNI_CRITICAL_SECTION",
    "SNI_HTTP_WAITFOR_",
    "SNI_LISTENER_ACCESS",
    "SNI_TASK_COMPLETION",
    "SOAP_READ",
    "SOAP_WRITE",
    "SOS_CALLBACK_REMOVAL",
    "SOS_DISPATCHER_MUTEX",
    "SOS_LOCALALLOCATORLIST",
    "SOS_MEMORY_USAGE_ADJUSTMENT",
    "SOS_OBJECT_STORE_DESTROY_MUTEX",
    "SOS_PHYS_PAGE_CACHE",
    "SOS_PROCESS_AFFINITY_MUTEX",
    "SOS_RESERVEDMEMBLOCKLIST",
    "SOS_SCHEDULER_YIELD",
    "SOS_SMALL_PAGE_ALLOC",
    "SOS_STACKSTORE_INIT_MUTEX",
    "SOS_SYNC_TASK_ENQUEUE_EVENT",
    "SOS_VIRTUALMEMORY_LOW",
    "SOSHOST_EVENT",
    "SOSHOST_INTERNAL",
    "SOSHOST_MUTEX",
    "SOSHOST_RWLOCK",
    "SOSHOST_SEMAPHORE",
    "SOSHOST_SLEEP",
    "SOSHOST_TRACELOCK",
    "SOSHOST_WAITFORDONE",
    "SQLCLR_APPDOMAIN",
    "SQLCLR_ASSEMBLY",
    "SQLCLR_DEADLOCK_DETECTION",
    "SQLCLR_QUANTUM_PUNISHMENT",
    "SQLSORT_NORMMUTEX",
    "SQLSORT_SORTMUTEX",
    "SQLTRACE_BUFFER_FLUSH",
    "SQLTRACE_FILE_BUFFER",
    "SQLTRACE_SHUTDOWN",
    "SQLTRACE_WAIT_ENTRIES",
    "SRVPROC_SHUTDOWN",
    "TEMPOBJ",
    "THREADPOOL",
    "TIMEPRIV_TIMEPERIOD",
    "TRACEWRITE",
    "TRAN_MARKLATCH_DT",
    "TRAN_MARKLATCH_EX",
    "TRAN_MARKLATCH_KP",
    "TRAN_MARKLATCH_NL",
    "TRAN_MARKLATCH_SH",
    "TRAN_MARKLATCH_UP",
    "TRANSACTION_MUTEX",
    "UTIL_PAGE_ALLOC",
    "VIA_ACCEPT",
    "VIEW_DEFINITION_MUTEX",
    "WAIT_FOR_RESULTS",
    "WAIT_XTP_CKPT_CLOSE",
    "WAIT_XTP_CKPT_ENABLED",
    "WAIT_XTP_CKPT_STATE_LOCK",
    "WAIT_XTP_GUEST",
    "WAIT_XTP_HOST_WAIT",
    "WAIT_XTP_OFFLINE_CKPT_LOG_IO",
    "WAIT_XTP_OFFLINE_CKPT_NEW_LOG",
    "WAIT_XTP_PROCEDURE_ENTRY",
    "WAIT_XTP_RECOVERY",
    "WAIT_XTP_TASK_SHUTDOWN",
    "WAIT_XTP_TRAN_COMMIT",
    "WAIT_XTP_TRAN_DEPENDENCY",
    "WAITFOR",
    "WAITFOR_TASKSHUTDOWN",
    "WAITSTAT_MUTEX",
    "WCC",
    "WORKTBL_DROP",
    "WRITE_COMPLETION",
    "WRITELOG",
    "XACT_OWN_TRANSACTION",
    "XACT_RECLAIM_SESSION",
    "XACTLOCKINFO",
    "XACTWORKSPACE_MUTEX",
    "XE_BUFFERMGR_ALLPROCESSED_EVENT",
    "XE_BUFFERMGR_FREEBUF_EVENT",
    "XE_DISPATCHER_CONFIG_SESSION_LIST",
    "XE_DISPATCHER_JOIN",
    "XE_DISPATCHER_WAIT",
    "XE_MODULEMGR_SYNC",
    "XE_OLS_LOCK",
    "XE_PACKAGE_LOCK_BACKOFF",
    "XTPPROC_CACHE_ACCESS",
    "XTPPROC_PARTITIONED_STACK_CREATE",
]


def _parameter_valuespec_mssql_blocked_sessions():
    return Dictionary(
        elements=[
            (
                "state",
                MonitoringState(
                    title=_("State if at least one blocked session"),
                    default_value=2,
                ),
            ),
            (
                "waittime",
                Tuple(
                    title=_("Levels for wait"),
                    help=_(
                        "The threshholds for wait_duration_ms. Will "
                        "overwrite the default state set above."
                    ),
                    default_value=(0, 0),
                    elements=[
                        Float(title=_("Warning at"), unit=_("seconds"), display_format="%.3f"),
                        Float(title=_("Critical at"), unit=_("seconds"), display_format="%.3f"),
                    ],
                ),
            ),
            (
                "ignore_waittypes",
                DualListChoice(
                    title=_("Ignore wait types"),
                    rows=40,
                    choices=[(entry, entry) for entry in mssql_waittypes],
                ),
            ),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="mssql_blocked_sessions",
        group=RulespecGroupCheckParametersApplications,
        is_deprecated=True,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_mssql_blocked_sessions,
        title=lambda: _("MSSQL Blocked Sessions"),
    )
)
