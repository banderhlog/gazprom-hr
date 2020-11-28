<?php

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class RequirementsSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        // types: select-years, select-options, write

        $requirements = [
            [
                'title' => 'Опыт',
                'type' => 'select-years'
            ],
            [
                'title' => 'Python',
                'type' => 'select-options',
                'options' => [
                    [
                        'title' => '2',
                        'type' => 'version'
                    ],
                    [
                        'title' => '3',
                        'type' => 'version'
                    ],
                    [
                        'title' => 'Flask',
                        'type' => 'framework'
                    ],
                    [
                        'title' => 'Django',
                        'type' => 'framework'
                    ]
                ]
            ],
            [
                'title' => 'PHP',
                'type' => 'select-options',
                'options' => [
                    [
                        'title' => 'Laravel',
                        'type' => 'framework'
                    ],
                    [
                        'title' => 'Symfony',
                        'type' => 'framework'
                    ],
                    [
                        'title' => 'Phalcon',
                        'type' => 'framework'
                    ],
                    [
                        'title' => 'Slim',
                        'type' => 'framework'
                    ],
                    [
                        'title' => '5.6',
                        'type' => 'version'
                    ],
                    [
                        'title' => '7.3',
                        'type' => 'version'
                    ],
                    [
                        'title' => 'Паттерны',
                        'type' => 'knowledge'
                    ],
                    [
                        'title' => 'ООП',
                        'type' => 'knowledge'
                    ],
                    [
                        'title' => 'Unit tests',
                        'type' => 'usage'
                    ]
                ]
            ],
            [
                'title' => 'JS',
                'type' => 'select-options',
                'options' => [
                    [
                        'title' => 'React',
                        'type' => 'framework'
                    ],
                    [
                        'title' => 'Vue',
                        'type' => 'framework'
                    ],
                    [
                        'title' => 'Angular',
                        'type' => 'framework'
                    ]
                ]
            ],
            [
                'title' => 'GIT'
            ],
            [
                'title' => 'Базы данных',
                'type' => 'select-options'
            ]
        ];


        foreach ($requirements as $requirement) {
            $options = $requirement['options'] ?? [];
            if (!empty($options)) {
                unset($requirement['options']);
            }
            $req = \App\Requirement::create($requirement);
            if (!empty($options)) {
                foreach ($options as $option) {
                    $option['requirement_id'] = $req->id;
                    \App\Option::create($option);
                }
            }

        }

    }
}
