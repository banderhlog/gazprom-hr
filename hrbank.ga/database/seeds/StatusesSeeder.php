<?php

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class StatusesSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        DB::table('statuses')->insert([
            [
                'title' => 'Обработка',
                'position' => 0
            ],
            [
                'title' => 'На утверждении',
                'position' => 1
            ],
            [
                'title' => 'Опубликована',
                'position' => 2
            ],
            [
                'title' => 'В архиве',
                'position' => 3
            ]
        ]);
    }
}
