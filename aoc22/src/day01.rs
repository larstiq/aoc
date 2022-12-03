#![allow(dead_code)]

use itertools::Itertools;

pub fn day01() {
    println!("day01 part1: {}", part1(&input()));
    println!("day01 part2: {}", part2(&input()));
}

fn input() -> String {
    std::fs::read_to_string("inputs/01").unwrap()
}

fn example() -> String {
    std::fs::read_to_string("examples/01").unwrap()
}

fn input_to_elves_itertools(input: &str) -> Vec<i64> {
    let elves: Vec<i64> = input.lines()
        .map(|line| line.parse::<i64>().ok())
        .group_by(|cal| cal.is_some())
        .into_iter()
        .map(|(_key, group)| group.flatten().sum())
        .collect();
    elves
}

fn input_to_elves_rawfor(input: &str) -> Vec<i64> {
    let mut elves: Vec<i64> = vec![0];

    for line in input.lines() {
        let mut elf = elves.last_mut().unwrap();
        if line.is_empty() {
            elves.push(0);
            elf = elves.last_mut().unwrap();
        } else {
            *elf += line.parse::<i64>().unwrap();
        }
    }
    elves
}


fn part1(input: &str) -> i64 {
    let max = *input_to_elves_itertools(input).iter().max().unwrap();
    max
}

fn part2(input: &str) -> i64 {
    let elves = input_to_elves_itertools(input);
    elves.iter().sorted().rev().take(3).sum()
}

#[test]
fn test_part1() {
    assert_eq!(part1(&example()), 24000);
}

#[test]
fn test_part2() {
    assert_eq!(part2(&example()), 45000);
}
