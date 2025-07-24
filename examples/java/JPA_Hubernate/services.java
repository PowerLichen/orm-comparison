public class PostPredicates {

    private static final QPost post = QPost.post;
    private static final QPostSection section = QPostSection.postSection;

    public static BooleanExpression filterByBlog(Long blogId) {
        return blogId == null ? null : post.blog.id.eq(blogId);
    }

    public static BooleanExpression filterByAuthors(List<Long> authorIds) {
        return (authorIds == null || authorIds.isEmpty()) ? null : post.author.id.in(authorIds);
    }

    public static BooleanExpression filterBySectionCode(String sectionCode, int offset) {
        if (sectionCode == null || sectionCode.isEmpty()) return null;

        var subQuery = JPAExpressions
            .select(section.post.id)
            .from(section)
            .where(section.sectionCode.eq(sectionCode));

        return offset > 0 ? post.id.notIn(subQuery) : post.id.in(subQuery);
    }

    public static BooleanExpression filterBySectionStatuses(List<SectionStatus> statuses) {
        if (statuses == null || statuses.isEmpty()) return null;

        return JPAExpressions
            .selectOne()
            .from(section)
            .where(
                section.post.id.eq(post.id)
                .and(section.permitComment.eq(true))
                .and(section.sectionStatus.in(statuses))
            )
            .exists();
    }
}

@Service
@RequiredArgsConstructor
public class PostService {

    private final PostRepository postRepository;

    public List<Post> getValidPosts(Long blogId, List<Long> authorIds, String sectionCode, int offset, String editTiming) {
        // 도메인 정책에 따른 상태 목록 생성
        List<SectionStatus> allowedStatuses = getAllowedStatuses(editTiming);

        // Predicate 조립
        BooleanExpression predicate = Expressions.allOf(
            PostPredicates.filterByBlog(blogId),
            PostPredicates.filterByAuthors(authorIds),
            PostPredicates.filterBySectionCode(sectionCode, offset),
            PostPredicates.filterBySectionStatuses(allowedStatuses)
        );

        int page = offset / 10;
        var pageable = PageRequest.of(page, 10, Sort.by(Sort.Direction.DESC, "postedAt"));

        return postRepository.findAll(predicate, pageable).getContent();
    }

    private List<SectionStatus> getAllowedStatuses(String editTiming) {
        return switch (editTiming) {
            case "검토중" -> List.of(SectionStatus.검토중, SectionStatus.검토완료, SectionStatus.게시됨);
            case "검토완료" -> List.of(SectionStatus.검토완료, SectionStatus.게시됨);
            default -> Collections.emptyList();
        };
    }
}