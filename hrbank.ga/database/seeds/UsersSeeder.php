<?php

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

class UsersSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        DB::table('users')->insert([
            [
                'name' => 'Заказчик',
                'email' => 'employer@hrbank.ga',
                'role_id' => 1,
                'password' => Hash::make('test')
            ],
            [
                'name' => 'HR',
                'email' => 'hr@hrbank.ga',
                'role_id' => 2,
                'password' => Hash::make('test')
            ]
        ]);
    }
}
