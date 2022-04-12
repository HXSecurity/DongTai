#!/usr/bin/env bats

setup_file() {
 # Initializing install 1.1.2 with schema hash 2a6c08ac348ac0f7f336588587eb05d5397ec84a
 echo "Start to install server..." >&3
 run ./dtctl install -v 1.3.1 -r 0 <<< 8088
}

teardown_file() { 
   echo "Start to clean test playground..." >&3
   run ./dtctl rm -d
}

@test "Print image version by: ./dtctl version" {
    run ./dtctl version
    [[ "${lines[1]}" =~ "1.3.1" ]]
}

@test "Print usage by: ./dtctl -h" {
    run ./dtctl -h
    [[ "${lines[1]}" == "[Info] Usage:" ]]
 }

@test "Export docker-compose.yaml by: ./dtctl file" {
    run ./dtctl file
    [ -f "docker-compose.yml" ]
}

@test "Export db schema by: ./dtctl dbschema" {
    run ./dtctl dbschema
    [ -f "export_db_schema.txt" ]
}

@test "Export dbhash by: ./dtctl dbhash" {
    run ./dtctl dbhash
    [[ "${lines[1]}" =~ "current db hash" ]]
}

# @test "Ugrade server by: ./dtctl upgrade -t 1.3.1" {
#     run ./dtctl dbhash
#     if [[ ! "${output}" =~ "150e0e2fa028ced9ae9f6246dce6a765041f9fb6" ]]; then
#       skip "Current db is not 1.1.2"
#     fi

#     ./dtctl upgrade -t 1.3.1
#     if [ ! -f "~/dongtai_iast_upgrade/dongtai_iast*" ]; then
#       echo "mysql backup error!"
#     fi
#     run ./dtctl dbhash
#     [[ "${lines[0]}" =~ "4b0735025ce3bf6b4294d76e82851493a64a940a" ]]
# }