#![allow(dead_code)]

use hashbag::HashBag;
use itertools::Itertools;
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

fn part2(input: &str) -> u32 {
    let mut total = 0;
    for (elf1, elf2, elf3) in input.lines().tuples() {
        // Whyyyy does HashSet<char> BitAnd require Eq (which is not on
        // char) and .intersection only does two sets at a time!? Argh!
        //
        // HashSet::from_iter(elf1.chars()).intersection(&HashSet::from_iter(elf2.chars())).intersection(HashSet::from_iter(elf3.chars()));
        // HashSet::from_iter(elf1.chars()) | HashSet::from_iter(elf2.chars())
        let mut bag = HashBag::new();
        bag.extend(elf1.chars().unique());
        bag.extend(elf2.chars().unique());
        bag.extend(elf3.chars().unique());
        bag.retain(|_, count| (count == 3) as usize);
        total += bag
            .drain()
            .last()
            .map(|(badge, _count)| priority(&badge))
            .unwrap();
    }
    total
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
