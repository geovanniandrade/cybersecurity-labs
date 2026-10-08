# Validação da versão v2

```text
VALIDAÇÃO LOCAL — DASHBOARD V2 — 07/10/2026

test_all_mutations_require_csrf (test_app.AssetTests.test_all_mutations_require_csrf) ... ok
test_duplicate_patrimony_rejected_case_insensitively (test_app.AssetTests.test_duplicate_patrimony_rejected_case_insensitively) ... ok
test_edit_keeps_id_date_and_updates_all_fields (test_app.AssetTests.test_edit_keeps_id_date_and_updates_all_fields) ... ok
test_health_headers_and_missing_asset (test_app.AssetTests.test_health_headers_and_missing_asset) ... ok
test_migration_preserves_original_schema_records_and_ids (test_app.AssetTests.test_migration_preserves_original_schema_records_and_ids) ... ok
test_missing_invalid_and_oversized_fields_are_rejected (test_app.AssetTests.test_missing_invalid_and_oversized_fields_are_rejected) ... ok
test_optional_price_blank_zero_and_exact_cents (test_app.AssetTests.test_optional_price_blank_zero_and_exact_cents) ... ok
test_register_details_and_restart_preserves_data (test_app.AssetTests.test_register_details_and_restart_preserves_data) ... ok
test_remove_get_never_deletes_and_confirmation_is_required (test_app.AssetTests.test_remove_get_never_deletes_and_confirmation_is_required) ... ok
test_search_filters_and_global_dashboard_totals (test_app.AssetTests.test_search_filters_and_global_dashboard_totals) ... ok
test_sql_text_and_html_are_handled_as_data (test_app.AssetTests.test_sql_text_and_html_are_handled_as_data) ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.258s

OK

Navegador Chromium: cadastro, detalhes, edição, confirmação de remoção e busca passaram.
Layout verificado em 1440 px e 390 px, sem rolagem horizontal da página. A tabela móvel permite rolagem interna.
Migração testada a partir do esquema inicial com preservação de ID, nome, responsável e data.
Build Docker v2 e atualização do volume real ainda pendentes de validação na VM.
Validação executada localmente antes da publicação nesta branch. A versão v2 ainda não foi aplicada na VM. Prévia contém apenas dados fictícios.

```
