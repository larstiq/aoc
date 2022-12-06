#![allow(dead_code)]

use std::collections::HashSet;

#[allow(unused_imports)]
use anyhow;

pub fn day03() {
    println!("day03 part1: {}", part1(&input()));
    println!("day03 part2: {}", part2(&input()));
}

fn priority(item: &char) -> u32 {
    match item {
        'a'..='z' => (*item as u32 - 'a' as u32) + 1,
        'A'..='Z' => (*item as u32 - 'A' as u32) + 27,
        _ => todo!(),
    }
}

fn part1(input: &str) -> u32 {
    input
        .lines() // Rucksack with two compartments per line.
        .map(|line| {
            let (left_line, right_line) = line.split_at(line.len() / 2);
            let left: HashSet<char> = HashSet::from_iter(left_line.chars());
            let right: HashSet<char> = HashSet::from_iter(right_line.chars());

            left.intersection(&right).last().map(priority).unwrap()
        })
        .sum()
}

fn part2(input: &str) -> i32 {
    0
}

fn input() -> String {
    std::fs::read_to_string("inputs/03").expect("inputs/03 to exist")
}

fn example() -> String {
    std::fs::read_to_string("examples/03").expect("examples/03 to exist")
}

#[test]
fn test_part1() {
    assert_eq!(157, part1(&example()));
    assert_eq!( 70, part2(&example()));
}
