# brannas-course-cccat17

description:
UC3 - Solicitar corrida
Ator: Passageiro
Input: passenger_id (account_id), from (lat, long), to (lat, long)
Output: ride_id

Regras:
* deve verificar se o account_id tem is_passenger true = OK
* deve verificar se já não existe uma corrida do passageiro em status diferente de "completed", se existir lançar um erro
* deve gerar o ride_id (uuid)
* deve definir o status como "requested"
* deve definir date com a data atual

UC4 - GetRide
Input: ride_id
Output: todos as informações da ride juntamente com os dados do passageiro e do motorista (inicialmente null, definido após o use case de AcceptRide)
