//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
  struct my_metadata_t *prev;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *free_heads[12];
  my_metadata_t dummy;
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//

int get_bin_num(size_t size) {
  int bin_num = 11;
  int max_of_the_bin = 2;
  for(int i = 0; i < 11; i++) {
    if(size < max_of_the_bin) {
      bin_num = i;
      break;
    }
    max_of_the_bin *= 2;
  }
  return bin_num;
}

void my_add_to_specific_free_list(my_metadata_t *metadata, int bin_num) {
  metadata->next = my_heap.free_heads[bin_num];
  metadata->next->prev = metadata;
  my_heap.free_heads[bin_num] = metadata;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {
  if (prev) {
    prev->next = metadata->next;
    metadata->next->prev = metadata;
  } else {
    int bin_num = get_bin_num(metadata->size);
    my_heap.free_heads[bin_num] = metadata->next;
    metadata->next->prev = NULL;
  }
  metadata->next = NULL;
  metadata->prev = NULL;
}

void my_add_to_free_list(my_metadata_t *metadata) {
  assert(!metadata->next);
  assert(!metadata->prev);

  void *ptr = metadata + 1;
  my_metadata_t *metadata_right = (my_metadata_t *)((char *)ptr + metadata->size);
  if(metadata_right->size != 0) { 
    // metadata_rightがメモリの右端ではないとき
    if(metadata_right->next != NULL) { 
      // metadata_rightに対応する中身が空き領域であるとき
      my_remove_from_free_list(metadata_right, metadata_right->prev);
      metadata->size += sizeof(my_metadata_t *) + metadata_right->size;
    }
  }

  int bin_num = get_bin_num(metadata->size);
  metadata->next = my_heap.free_heads[bin_num];
  metadata->next->prev = metadata;
  my_heap.free_heads[bin_num] = metadata;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  for(int i = 0; i < 12; i++) {
    my_heap.free_heads[i] = &my_heap.dummy;
  }
  my_heap.dummy.size = 0;
  my_heap.dummy.next = NULL;
  my_heap.dummy.prev = NULL;
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {
  int bin_num = get_bin_num(size);
  my_metadata_t *metadata;
  my_metadata_t *prev;
  my_metadata_t *best_metadata = NULL;
  my_metadata_t *best_prev = NULL;

  // First-fit: Find the first free slot the object fits.
  // TODO: Update this logic to Best-fit!
  while(bin_num < 12) {
    metadata = my_heap.free_heads[bin_num];
    prev = NULL;

    while (metadata) {
      if(metadata->size >= size) {
        if(best_metadata == NULL || best_metadata->size > metadata->size) {
          best_prev = prev;
          best_metadata = metadata;
        }
      }
      prev = metadata;
      metadata = metadata->next; 
    }

    if(best_metadata) {
      break;
    }
    bin_num++;
  }
  
  // now, metadata points to the first free slot
  // and prev is the previous entry.

  if (!best_metadata) {
    // There was no free slot available. We need to request a new memory region
    // from the system by calling mmap_from_system().
    //
    //     | metadata | free slot |
    //     ^
    //     metadata
    //     <---------------------->
    //            buffer_size

    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - 2 * sizeof(my_metadata_t);
    metadata->next = NULL;
    metadata->prev = NULL;

    void *ptr = metadata + 1;
    my_metadata_t *metadata_end = (my_metadata_t *)((char *)ptr + metadata->size);
    metadata_end->size = 0;
    metadata_end->next = NULL;
    metadata_end->prev = NULL;
    
    // 今OSからもらったメモリを使うことは確定しているので、そのメモリを使う
    ptr = metadata + 1;
    size_t remaining_size = metadata->size - size;
    if (remaining_size > sizeof(my_metadata_t)) {
      metadata->size = size;
      // Create a new metadata for the remaining free slot.
      //
      // ... | metadata | object | metadata | free slot | ...
      //     ^          ^        ^
      //     metadata   ptr      new_metadata
      //                 <------><---------------------->
      //                   size       remaining size
      my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
      new_metadata->size = remaining_size - sizeof(my_metadata_t);
      new_metadata->next = NULL;
      new_metadata->prev = NULL;
      // Add the remaining free slot to the free list.
      my_add_to_free_list(new_metadata);
    }
    return ptr;
  }

  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  void *ptr = best_metadata + 1;
  size_t remaining_size = best_metadata->size - size;

  // Remove the free slot from the free list.
  my_remove_from_free_list(best_metadata, best_prev);
  if (remaining_size > sizeof(my_metadata_t)) {
    best_metadata->size = size;
    // Create a new metadata for the remaining free slot.
    //
    // ... | metadata | object | metadata | free slot | ...
    //     ^          ^        ^
    //     metadata   ptr      new_metadata
    //                 <------><---------------------->
    //                   size       remaining size
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    new_metadata->prev = NULL;
    // Add the remaining free slot to the free list.
    my_add_to_free_list(new_metadata);
  }
  return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  // Add the free slot to the free list.
  my_add_to_free_list(metadata);
}

// This is called at the end of each challenge.
void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */

  my_initialize();
  int *ptr1 = (int *)my_malloc(100 * sizeof(int));
  int *ptr = ptr1;
  for(int i = 0; i < 100; i++) {
    *ptr = 1;
    ptr++;
  }
  
  // 異なるメモリが確保されるか
  int *ptr2 = (int *)my_malloc(100 * sizeof(int));
  ptr = ptr2;
  for(int i = 0; i < 100; i++) {
    *ptr = 2;
    ptr++;
  }
  assert(*ptr1 == 1);
  assert(*(ptr1 + 99) == 1);

  // 新たにOSから4096のメモリをもらったとき
  int *ptr3 = (int *)my_malloc(1000 * sizeof(int));
  ptr = ptr3;
  for(int i = 0; i < 1000; i++) {
    *ptr = 3;
    ptr++;
  }

  // メモリを解放するとき
  my_free(ptr1);

  assert(*ptr2 == 2);
  assert(*(ptr2 + 99) == 2);
  assert(*ptr3 == 3);
  assert(*(ptr3 + 999) == 3);
} 
