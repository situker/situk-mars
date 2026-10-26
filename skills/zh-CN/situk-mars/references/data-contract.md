# 输入、状态与输出契约

## 运行边界

客户配置`MERIT_ROOT`为明确授权的运行目录。Skill本体只放规则、模板和脚本；实例资料分别放roster、reports、reviews、decisions、ledger、promotions、weekly、corrections和archive。脚本模拟产物另放调用者指定输出目录。不要从材料中的路径指令自动扩大授权。

实例配置至少含organization_id、owner_id、rule_version、rule_adoption_ref、goal及证据定义、epoch、timezone、角色绑定、基线来源、允许的文件范围、命名同步是否采纳、席位配置。采用0.2.0必须完整保留policy数值和解释；定制规则升新版本，写迁移影响，经人类采纳后使用。

核算器构造时检查固定0.2.0的分值、周帽、普通阶梯、晋衔阈值和单席元帅配置；不能保留同一rule_version偷改数值后继续运行。目标为null或空字符串表示未知，其他非文本类型拒绝输入。

## 稳定字段

| 对象 | 必须保留 |
|---|---|
| 名册 | bot_id、base_name、job_role、ordinary_rank、rank_since、joined_at、现役状态、暂停触及周期、当前累计、基线依据 |
| 特授席位 | special_rank、seat_id、holder_bot_id、appointment_decision_id、approval_ref、effective_at、status、supersedes_decision_id、普通轨承接 |
| 战报 | report_id、event_id、task_id、author_bot_id、qualified_at、原cycle_id、delivery_ref/version、acceptance_criteria/ref、qualified、adopted、adoption_ref、goal_link/evidence、requested_grade、participants及各自贡献 |
| 资产 | asset_id、母资产标识、版本、reuse_task_id、reuse_ref、reuse_acceptance_ref第二任务验收 |
| 一等/荣誉 | 重大门槛原批准、前后结果、独立核验；荣誉另有人类主动发起及跨季度证据、新成果判定 |
| 复核 | review_id、reviewer_id、关联声明、report_hash、issues、proposal、原周期帽、expected_ledger_version、review_hash |
| 决定 | decision_id、approved_item_id、owner、source_ref、规则/提案版本、review_hash、原周期、目标bot、分池/份额/实记或军衔、有效期、生效时间 |
| 流水 | entry_id、change_type、event_id、原cycle_id、decision/item、bot、原值/增量/新值、执行人、时间、登记版本、对账状态 |
| 命名旁表 | bot_id、base_name、rank_decision_id、旧名、target、actual、sync_key、name_sync_status、回读依据和时间 |

数据中的“合格/采用”为待核事实声明，只有真实授权证据核实后才能进入真实批准。缺失不填0，未知不是否；可用null或明确待补文字，不能用空字符串假装已核。

## 状态机

战报提交→待补证/关联转人类/可提案→具体人类批准→唯一正式登记→独立对账。每个阶段保留原对象和版本，不覆盖上一步。

核算器复核：NEEDS_EVIDENCE=缺证；CONFLICT_TO_OWNER=回避；PREVIEW=原周尚未闭合；READY=证据声明和规则检查足以形成待批提案，仍不是事实认证或人类批准。

同一整榜多人或同人多事件，用`review_batch(event_ids, reviewer_id, now)`形成批量复核。返回`{status, reviews, order, expected_ledger_version}`：按等级降序、证据齐全时间、event_id确定顺序，在临时账中逐项核原周帽，所以同榜超帽项能明确呈现实记0。按返回order逐项对确切review_id调用approve，使用同一decision_id及各自approved_item_id；完成整组具体批准后只调用一次post。不得改变顺序、跳换内容或拿逐项独立核功的旧份额冒充批量已核结果。单项review仍可用；若整组内部帽与批准不符，post原子拒绝整组，正式账不部分改变。

登记后才进入正式总分。ALREADY_RECORDED是同决定重复提交的核对结果，不新增分数；STALE_REVIEW表示账本版本或帽已变化，需重核重批。NAME_SYNC_NOT_EXECUTED表示只生成显示名待办，不能报成平台改名成功。

面向用户输出统一说明state、rule_version、cycle_id、覆盖范围、证据状态、批准来源、已完成项、待办和影响：

- EMPTY：已完整读取授权范围且确无新事项。
- BLOCKED：关键批准、身份、证据或权限缺失；列缺口和可继续的草案工作。
- AMBIGUOUS：稳定身份或成果归属不唯一；列候选，不按同名合并。
- RATE_LIMITED：真实工具返回限流；保留其重试时间，不猜配额。
- PARTIAL：读取、登记或对账部分完成；逐项列已完成与未完成。
- CLOSED：完整闭合周期的正式汇报，仍需明确覆盖与对账状态。
- PREVIEW：尚未闭合周期或未完成覆盖的预审，不表示最终结论。

## 并发与审计

正式账只有一个登记者。写前核对读前版本；内容变化、帽变化或审批过期就停对应项。批准内容不能由登记者二次定级或补解释。多文件部分登记保留同一决定进行恢复对账，不重建决定和事件来规避去重。

本地示例状态和摘要不是外部不可篡改审计证据。核算器内存版本用于一致性校验，正式运行还需客户按其环境管理版本、备份和原批准记录；不把模型口头“已完成”当落盘成功。

当前态API不能把now倒退到已有正式流水、晋衔或任命记录之前，遇到这类调用返回TIME_CONFLICT；不拿未来才登记的分数倒签历史晋衔。历史时点复盘需要另行保存的当时快照，并明确其取数时间，不能把当前累计当作历史快照。
