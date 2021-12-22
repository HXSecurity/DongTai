#!/usr/bin/env bats

setup_file() {
 # Initializing install 1.1.2 with schema hash 2a6c08ac348ac0f7f336588587eb05d5397ec84a

 run ./dtctl install -v 1.1.2 <<< 8088

 while :; do
    echo "output:$output" >&3
    run ./dtctl dbhash    
    if [[ "${output}" =~ "2a6c08ac348ac0f7f336588587eb05d5397ec84a" ]]; then
      echo "mysql instance ready!" >&3
      break
    fi
    echo "Waiting for mysql to be ready,sleep 10s..." >&3
    sleep 10
  done
}

teardown_file() { 
   echo "Start to clean test playground..." >&3
   run ./dtctl rm
}

@test "Print image version by: ./dtctl version" {
    run ./dtctl version
    [[ "${lines[0]}" =~ "1.1.2" ]]
}

@test "Print usage by: ./dtctl -h" {
    run ./dtctl -h
    [[ "${lines[0]}" == "[Info] Usage:" ]]
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
    [[ "${lines[0]}" =~ "current db hash" ]]
}

@test "Ugrade server by: ./dtctl upgrade -t 1.1.3" {
    run ./dtctl dbhash
    if [[ ! "${output}" =~ "2a6c08ac348ac0f7f336588587eb05d5397ec84a" ]]; then
      skip "Current db is not 1.1.2"
    fi

    ./dtctl upgrade -t 1.1.3
    if [ ! -f "~/dongtai_iast_upgrade/dongtai_iast*" ]; then
      echo "mysql backup error!"
    fi
    run ./dtctl dbhash
    [[ "${lines[0]}" =~ "4b0735025ce3bf6b4294d76e82851493a64a940a" ]]
}