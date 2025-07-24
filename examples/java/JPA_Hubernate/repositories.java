public interface PostRepository extends JpaRepository<Post, Long>, QuerydslPredicateExecutor<Post> {
    // 별도 구현 없이 Predicate 기반 조회 지원
}