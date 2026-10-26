# 花名册模板

本表从空白建档。稳定身份、岗位、普通军衔、特授席位和实际平台权限分别保存。不得从现有显示名反推已授军衔，也不得把不明旧记录重置为列兵。

- `organization_id`：<编制稳定标识>
- `rule_version`：<规则版本>
- `roster_version`：<本次花名册版本/内容 hash>
- `merit_epoch`：<已批准的新功起算时间，含时区>
- `timezone`：Asia/Singapore
- 起算批准：<人类批准原记录>
- 已读范围/未覆盖项：<清单与观察时间>

| 字段 | 一位机器人的记录 |
|---|---|
| `bot_id` | <稳定 ID，不随改名变动> |
| `base_name` | <经核实的原职责名> |
| `job_role` | <业务岗 / commander / military_officer> |
| `ordinary_rank` | <列兵至中校；未知则待核> |
| `ordinary_rank_effective_at` | <最近一次有效普通军衔生效时间> |
| `ordinary_rank_decision_id` | <入列或晋降衔决定> |
| `active_intervals` | <现役起止；暂停/恢复时间，不省略> |
| `special_rank` | <空 / 元帅> |
| `seat_id` | <空 / commander-marshal-01> |
| `appointment_decision_id` | <特授任命或撤销决定> |
| `special_effective_at` / `special_status` | <生效时间 / 空缺、有效、已撤销、待核> |
| `formal_points` | <由已批流水重算；不含草案及已批未登记项> |
| `approved_duties` | <当前职责及批准依据> |
| `permission_enforcement` | <POLICY_ONLY / 经核实的技术控制及证据> |
| `display_name_target` | <base_name〔已核实有效军衔〕> |
| `display_name_actual` | <独立观察所得；未读取写未知> |
| `name_sync_status` | <NOT_REQUESTED / PENDING / MATCHED / BLOCKED / FAILED> |
| `name_sync_key` | <bot_id + rank_decision_id + display-name> |
| `name_readback_ref` / `observed_at` | <实际名字回读证据 / 时间> |

元帅特授席位同一编制最多一人，可空缺，不加分、不重置普通在阶起算，不附带权限。岗位名叫“元帅”不构成任命；军务官岗位也不规定其普通军衔。

显示名由 `base_name` 与最新有效军衔生成，不能在已有名字上连续追加。图标只用于榜单展示，统一写“🏅 等级文字”；拟授项目标“拟授/待批”。本地模拟只生成目标名，实际名字保持模拟观察值。未批准、无能力或没有当前动作授权时，不改真实名字。

入列附件：职责范围、交付及验收标准、新功起算、初始普通军衔和批准指针。完整周从有效普通在阶起算后计，部分周与触及暂停的周不计。不因无任务、无战报处罚机器人。
